import glob
import os
import struct
import re
from collections import Counter
from queue import Queue
from xmlrpc.client import ServerProxy
import base64
import zlib
import time


def is_video_file(filename):
    ''' Checks if the given file name is a valid video file or not, based on its extension.'''

    video_extns = [
        '.avi',
        '.divx',
        '.mkv',
        '.mp4',
        '.ogg',
        '.rm',
        '.rmvb',
        '.vob',
        '.x264',
        '.xvid',
        '.wmv',
        '.mov',
        '.mpeg',
    ]
    if os.path.splitext(filename)[1].lower() in video_extns:
        return True


def calc_file_hash(filepath):
    ''' Calculates the hash value of a movie.
        Edited from from OpenSubtitles's own examples:
        http://trac.opensubtitles.org/projects/opensubtitles/wiki/HashSourceCodes
        '''

    try:
        longlongformat = 'q'  # long long
        bytesize = struct.calcsize(longlongformat)

        f = open(filepath, 'rb')

        filesize = os.path.getsize(filepath)
        filehash = filesize

        if filesize < 65536 * 2:
            raise Exception('SizeError: Minimum file size must be 120Kb'
                            )

        for x in range(65536 // bytesize):
            buffer = f.read(bytesize)
            (l_value, ) = struct.unpack(longlongformat, buffer)
            filehash += l_value
            filehash = filehash & 0xFFFFFFFFFFFFFFFF  # to remain as 64bit number

        f.seek(max(0, filesize - 65536), 0)
        for x in range(65536 // bytesize):
            buffer = f.read(bytesize)
            (l_value, ) = struct.unpack(longlongformat, buffer)
            filehash += l_value
            filehash = filehash & 0xFFFFFFFFFFFFFFFF

        f.close()
        filehash = '%016x' % filehash
        return filehash
    except IOError:
        raise


tv_show_regex = re.compile(r"(?:[^\\]\\)*(?P<SeriesName>.*) S?(?P<SeasonNumber>[0-9]+)(?:[ .XE]+(?P<EpisodeNumber>[0-9]+))(?P<Teams>.*)", re.I)


movie_regex = re.compile('(?P<movie>.*)[\.|\[|\(| ]{1}(?P<year>(?:(?:19|20)[0-9]{2}))(?P<teams>.*)', re.IGNORECASE)


def unicode(arg):
    return str(arg)


def clean_name(name):
    ''' Cleans the file name of non alpha numeric characters and extra spaces.'''

    name = re.sub('[\W_]+', ' ', unicode(name.lower()))
    name = re.sub(r"\s+", ' ', name)
    return name


def guess_file_data(filename):
    filename = clean_name(filename)
    matches_tvshow = tv_show_regex.match(filename)
    matches_movie = movie_regex.match(filename)

    if matches_tvshow and not matches_movie:
        (tvshow, season, episode, teams) = matches_tvshow.groups()
        teams = teams.split()
        data = {
            'type': 'tvshow',
            'name': tvshow.strip(),
            'season': int(season),
            'episode': int(episode),
            'teams': teams,
        }
    elif matches_movie:
        (movie, year, teams) = matches_movie.groups()
        teams = teams.split()
        part = None
        if 'cd1' in teams:
            teams.remove('cd1')
            part = 1
        if 'cd2' in teams:
            teams.remove('cd2')
            part = 2
        data = {
            'type': 'movie',
            'name': movie.strip(),
            'year': year,
            'teams': teams,
            'part': part,
        }
    else:
        data = {'type': 'unknown', 'name': filename, 'teams': []}

    return data


def check_tvshow(filename):
    ''' Checks if the given file name is a valid tv show episode or not.'''

    fname = unicode(filename.lower())
    guessed_file_data = guess_file_data(fname)
    return guessed_file_data['type'] == 'tvshow'


def catch_all(site, files):
    try:
        print(site)
    except Exception as e:
        print(e)


LANGUAGES = {
    u'English': ('1', 'eng'),
    u'French': ('8', 'fre'),
    u'Greek': ('27', 'ell'),
    u'Spanish': ('4', 'spa'),
    u'Portuguese(Br)': ('10', 'pob'),
    u'Italian': ('7', 'ita'),
}


def save_subs(content, full_path, other_details=None):
    open(full_path, 'wb').write(content)


class OpenSubtitles:

    api_url = 'http://api.opensubtitles.org/xml-rpc'
    login_token = None
    server = None

    def __init__(self, parent=None):
        self.stopping = False

    def process(self, files_list, lang='English'):
        self.moviefiles = files_list
        self.imdbid_to_hash = {}
        self.lang = LANGUAGES[lang][1]
        if not self.stopping:
            self.run()

    def __del__(self):
        if self.login_token:
            self.logout()

    def stopTask(self):
        self.stopping = True

    def run(self):
        try:
            if not self.login_token:
                self.login()
            self.search_subtitles()
        except Exception as e:
            print(e, "first exception")

    def login(self):
        '''Log in to OpenSubtitles.org'''

        self.server = ServerProxy(self.api_url, verbose=False)

        try:
            resp = self.server.LogIn('', '', 'en', 'PySubD v2.0')
            self.check_status(resp)
            self.login_token = resp['token']
        except Exception as e:
            if e.args[0] == 11004:
                print("No Internet Connection Found", 'error')
            else:
                print(str(e), 'error')

    def logout(self):
        '''Log out from OpenSubtitles'''

        print('Logging out...', 'info')
        resp = self.server.LogOut(self.login_token)
        self.check_status(resp)

    def check_status(self, resp):
        '''Check the return status of the request.
        Anything other than "200 OK" raises a UserWarning
        '''

        if resp['status'].upper() != '200 OK':
            print('Response error')

    def _query_opensubs(self, search):
        results = []
        while search[:500]:
            if not self.stopping:
                try:
                    tempresp = self.server.SearchSubtitles(self.login_token, search[:500])
                except Exception as e:
                    if e.args[0] == 11004:
                        print("No Internet Connection Found", 'error')
                    else:
                        print(str(e), 'error')
                    return results
                if tempresp['data']:
                    results.extend(tempresp['data'])
                self.check_status(tempresp)
                search = search[500:]
            else:
                return []

        return results

    def clean_results(self, results):
        subtitles = {}
        user_ranks = {'administrator': 1,
                      'platinum member': 2,
                      'vip member': 3,
                      'gold member': 4,
                      'trusted': 5,
                      'silver member': 6,
                      'bronze member': 7,
                      'sub leecher': 8,
                      '': 9, }

        for result in results:
            if result['SubBad'] != '1':
                movie_hash = result.get('MovieHash')
                if not movie_hash:
                    movie_hash = self.imdbid_to_hash[int(result['IDMovieImdb'])]
                subid = result['IDSubtitleFile']
                downcount = int(result['SubDownloadsCnt'])
                rating = float(result['SubRating'])
                IDMovieImdb = int(result.get('IDMovieImdb', 0))

                if rating and rating < 8:
                    # Ignore poorly rated subtitles, while not
                    # penalizing the ones that haven't yet been rated
                    continue

                user_rank = user_ranks[result['UserRank']]
                subtitles.setdefault(movie_hash, []).append((subid, downcount, rating, user_rank, IDMovieImdb))

        return subtitles

    def search_subtitles(self):
        search = []
        cnt = Counter()
        for video_file_details in self.moviefiles.values():
            video_file_details['sublanguageid'] = self.lang
            search.append(video_file_details)

        results = self._query_opensubs(search)

        subtitles = self.clean_results(results)
        print(subtitles, "clean_results")
        for hash, found_matches in subtitles.items():
            for dicts in found_matches:
                cnt[dicts[4]] += 1

            most_common = cnt.most_common(1)[0][0]
            expectedResult = [d for d in found_matches if d[4] == most_common]
            print(expectedResult, "expected")
            subtitles[hash] = sorted(found_matches, key=lambda x: (x[3], -x[2], -x[1]))[0]

        for (hash, filedetails) in self.moviefiles.items():
            if not self.stopping:
                if subtitles.get(hash):
                    print('Saving subtitles for %s' % filedetails['file_name'], 'success')
                    subtitle = self.download_subtitles([subtitles[hash][0]])
                    save_subs(subtitle, filedetails['save_subs_to'], subtitles[hash])
                else:
                    print("no sub found")
            else:
                return

    def download_subtitles(self, subparam):
        resp = self.server.DownloadSubtitles(self.login_token, subparam)
        self.check_status(resp)
        decoded = base64.standard_b64decode(resp['data'][0]['data'].encode('ascii'))
        decompressed = zlib.decompress(decoded, 15 + 32)
        return decompressed


def process_queue(queue):
    addic7ed_list = []
    opensubs_dict = {}

    for video in queue:
        if video['type'] == 'Addic7ed':
            addic7ed_list.append(video)

    # if addic7ed_list:
    #     catch_all('Addic7ed', addic7ed_list)

    # time.sleep(0.01)  # To prevent race condition

    for video in queue:
        if video['type'] == 'OpenSubtitles':
            opensubs_dict[video['moviehash']] = video

    print(opensubs_dict)
    # if opensubs_dict:

    #     sub = OpenSubtitles()
    #     sub.process(opensubs_dict)


movie_queue = []


def add_to_processing_queue(filename, parentdir):  # called by check_and_add and creates _queue

    filehash = calc_file_hash(os.path.join(parentdir, filename))
    filesize = os.path.getsize(os.path.join(parentdir, filename))
    save_to_path = os.path.join(parentdir, os.path.splitext(filename)[0] + '.srt')
    movie_queue.append({'file_name': filename, 'type': 'Addic7ed' if check_tvshow(filename) else 'OpenSubtitles', 'save_subs_to': save_to_path, 'moviehash': filehash,
                        'moviebytesize': str(filesize)})


cancelled = False


def check_and_add(videos_pathlist):
    for path in videos_pathlist:
        if os.path.isfile(path):
            if is_video_file(path):
                add_to_processing_queue(os.path.basename(path), os.path.dirname(path))

        else:
            print(path, "path else")
            for (root, _, files) in os.walk(path):
                break
                for filename in files:
                    if is_video_file(filename):
                        add_to_processing_queue(filename, root)
                        print(filename, "file name")


def file_paths(input_path):          # mine
    file_list = []
    for folderName, subfolders, filenames in os.walk(input_path):
        for filename in filenames:
            path = folderName + '\\' + filename
            file_list.append(path)
    return file_list


input_path = "E:\\To Catch A Thief (1955) [BluRay] [720p] [YTS.AM]"

check_and_add(file_paths(input_path))


process_queue(movie_queue)
