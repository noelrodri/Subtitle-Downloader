

# name = input('Enter the name of user or group: ')
# msg = input('Enter your message : ')


# input('Enter anything after scanning Qr code')


# from selenium import webdriver

# driver = webdriver.Chrome()
# # driver.get('https://web.whatsapp.com/')

# name = input('Enter the name of user or group: ')
# msg = input('Enter your message : ')


# input('Enter anything after scanning Qr code')


# user = driver.find_element_by_xpath('//span[@title = "{}"]'.format("Nazi lives Matter"))
# user.click()

# msg_box = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')

# button = driver.find_element_by_class_name('compose-brn-send')

# msg_box.send_keys(msg)
# button.click()

# divs = soup.select('._3zb-j')[-1]


def click_button():
    button = driver.find_element_by_class_name('_35EW6')
    button.click()


def last_message():
    url = driver.page_source
    soup = bs(url, "lxml")
    divs = soup.select('._3zb-j')[-1]
    if divs:
        return divs.get_text()


# with open("jokes.txt", 'r') as f:
#     for line in f:
#         print(line)


word_dictionary = {
    "hi": "hi",

    "?": "?",

    "wrong": "nothing",

    "mosses": "why did he take so long?",

    "python code": "no man its not",

    "do something": "for sure",

    " long since": "too long man",

    "need": "true true",

    "high": "no man",

    "drink": "its not good for health man",

    "take long": "ok lets see",

    "abhimanyu": "what a prick man he is",

    "bihari": "they are the worst man",

    "bihar": "its such a dirty place"


}


VIDEO_EXTENSIONS = [
    ".avi", ".mp4", ".mkv", ".mpg",
    ".mpeg", ".mov", ".rm", ".vob",
    ".wmv", ".flv", ".3gp", ".3g2"
]

import glob
import os
# file_list = []

# input_path = 'E:\\folder for subtitles\\'


# print(file_list)
# file_handler(final_list)

# request = "https://subscene.com/subtitles/release?q=" + "The.Gentlemen.2019.720p.WEBRip.x264.AAC-[YTS.MX]"


# movie_name = "The.Gentlemen.2019.720p.WEBRip.x264.AAC-[YTS.MX]"


# yts_re = re.compile(r'yts', re.I)

# print(re.split(movie, movie_name)[0])


# os.unlink("brooklyn-nine-nine-sixth-season_HI_english-1947902.zip")


# file_path = "E:/folder for subtitles/"
# language = "english"
# arr = bytes("hello", 'utf-8')
# subfile = open(file_path + " {}.zip".format(language), 'wb')
# for i in range(10):
#     subfile.write(arr)

# subfile.close()

# import zipfile

# zip_ = zipfile.ZipFile(file_path + "{}.zip".format(language))
# zip_.extractall(file_path)
# zip_.close()
# os.unlink(file_path + "{}.zip".format(language))


# print("The integer conversion results in : " + str(bytes(a)))

# from xmlrpc.client import ServerProxy, Error
# api_url = 'http://api.opensubtitles.org/xml-rpc'
# server = ServerProxy(api_url, verbose=False)
# # resp = server.LogIn('', '', 'en', 'PySubD v2.0')
# # login_token = resp['token']

# # print(login_token)
# login_token = 'Q-Jfw-deAlA-,MxzDr6qY8-m5p2'

# tempresp = self.server.SearchSubtitles(self.login_token, search[:500])
# resp = server.LogOut(login_token)
# print(resp)

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


import struct


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


import re
from collections import Counter

tv_show_regex = re.compile(r"(?:[^\\]\\)*(?P<SeriesName>.*) S?(?P<SeasonNumber>[0-9]+)(?:[ .XE]+(?P<EpisodeNumber>[0-9]+))(?P<Teams>.*)", re.IGNORECASE)


movie_regex = re.compile('(?P<movie>.*)[\.|\[|\(| ]{1}(?P<year>(?:(?:19|20)[0-9]{2}))(?P<teams>.*)', re.IGNORECASE)


def unicode(arg):
    return str(arg)


def clean_name(name):
    ''' Cleans the file name of non alpha numeric characters and extra spaces.'''

    # pattern = re.compile('[\W_]+')
    name = re.sub('[\W_]+', ' ', unicode(name.lower()))
    name = re.sub(r"\s+", ' ', name)
    return name


def guess_file_data(filename):
    filename = clean_name(filename)
    matches_tvshow = tv_show_regex.match(filename)
    matches_movie = movie_regex.match(filename)

    if matches_tvshow and not matches_movie:
        (tvshow, season, episode, teams) = matches_tvshow.groups()
        # print(tvshow)
        # print(season)
        # print(episode)
        # print(teams)
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


from queue import Queue

_queue = Queue()


def add_to_processing_queue(filename, parentdir):  # called by check_and_add and creates _queue
    # communicator.updategui.emit('Found: %s' % filename, 'info')
    # communicator.found_video_file.emit(filename)

    filehash = calc_file_hash(os.path.join(parentdir, filename))
    filesize = os.path.getsize(os.path.join(parentdir, filename))
    save_to_path = os.path.join(parentdir, os.path.splitext(filename)[0] + '.srt')
    _queue.put({'file_name': filename, 'type': 'Addic7ed' if check_tvshow(filename) else 'OpenSubtitles', 'save_subs_to': save_to_path, 'moviehash': filehash,
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
                    if not cancelled:
                        if is_video_file(filename):
                            add_to_processing_queue(filename, root)
                            print(filename, "file name")
                            # print("hi")

                    else:
                        return


# movie_list = ['E:/folder for subtitles\\The.Gentlemen.2019.720p.WEBRip.x264.AAC-[YTS.MX].mp4',
#               'E:/folder for subtitles\\Brooklyn.Nine-Nine.S06E09.The.Golden.Child.720p.AMZN.WEB-DL.DDP5.1.H.264-NTb[eztv].mkv',
#               'E:/folder for subtitles\\mcmillions\\McMillions.S01E01.iNTERNAL.480p.x264-mSD[eztv].mkv']
# check_and_add(movie_list)


def file_paths(input_path):          # mine
    file_list = []
    for folderName, subfolders, filenames in os.walk(input_path):
        for filename in filenames:
            path = folderName + '\\' + filename
            file_list.append(path)
    return file_list


input_path = "E:\\movies\\Men In Black International (2019) [WEBRip] [720p] [YTS.LT]"

check_and_add(file_paths(input_path))


# for x in _queue.queue:
#     print(x)

# print(_queue.qsize())

import time


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

from xmlrpc.client import ServerProxy
import base64
import zlib
from operator import itemgetter


def save_subs(content, full_path, other_details=None):
    ''' Saves the content to the specified full path '''

    open(full_path, 'wb').write(content)


# def multikeysort(items, columns):
#     '''Sorts a list a of dictionary based on multiple keys.
#        A column can be reverse sorted by specifying - in front of the field name.'''

#     comparers = [((itemgetter(col[1:].strip()), -1) if col.startswith('-') else (itemgetter(col.strip()), 1)) for col in columns]

#     def cmp(a, b):
#         return (a > b) - (a < b)

#     def comparer(left, right):
#         for (fn, mult) in comparers:
#             result = cmp(fn(left), fn(right))
#             if result:
#                 return mult * result
#         else:
#             return 0

#     return sorted(items, key=comparer)

# def multikeysort(items, columns):
#     descended_sort = sorted(items, key=itemgetter('overlap', 'user_rank', 'downcount'))
#     lowest_value = descended_sort[0]['user_rank']

#     def compare_function(dicts):
#         if dicts["user_rank"] == lowest_value:
#             return True

#         else:
#             False

#     def compare_function2(dicts):
#         if dicts["rating"] >= 10:
#             return True

#         else:
#             False

#     rating_sort = sorted(filter(compare_function, descended_sort), key=itemgetter('rating'), reverse=True)
#     return sorted(filter(compare_function2, rating_sort), key=itemgetter('downcount'), reverse=True)

from functools import cmp_to_key


def multikeysort(items, columns):
    comparers = [((itemgetter(col[1:].strip()), -1) if col.startswith('-') else (itemgetter(col.strip()), 1)) for col in columns]

    def cmp(a, b):
        return (a > b) - (a < b)

    def comparer(left, right):
        comparer_iter = (cmp(fn(left), fn(right)) * mult for fn, mult in comparers)
        return next((result for result in comparer_iter if result), 0)

    return sorted(items, key=cmp_to_key(comparer))


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

    def clean_results(self, results, imdb=False):
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

                if imdb:
                    cleaned_release_name = clean_name(result['MovieReleaseName'])
                    file_name = self.moviefiles[movie_hash]['file_name']
                    cleaned_file_name = clean_name(file_name)
                    overlap = len(set.intersection(set(cleaned_release_name), set(cleaned_file_name)))
                else:
                    overlap = 0

                subtitles.setdefault(movie_hash, []).append({
                    'subid': subid,
                    'downcount': downcount,
                    'rating': rating,
                    'user_rank': user_rank,
                    'IDMovieImdb': IDMovieImdb
                })

                # subtitles.setdefault(movie_hash, []).append((subid, downcount, rating, user_rank))

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
                cnt[dicts['IDMovieImdb']] += 1

            most_common = cnt.most_common(1)[0][0]
            expectedResult = [d for d in found_matches if d['IDMovieImdb'] == most_common]
            print(expectedResult, "expected")
            subtitles[hash] = multikeysort(expectedResult, ['user_rank', '-rating', '-downcount'])[0]
            # subtitles[hash] = sorted(found_matches, key=lambda x: (x[3], -x[2], -x[1]))[0]

        for (hash, filedetails) in self.moviefiles.items():
            if not self.stopping:
                if subtitles.get(hash):
                    print('Saving subtitles for %s' % filedetails['file_name'], 'success')
                    # print([subtitles[hash][0]], "selected subtitle")
                    subtitle = self.download_subtitles([subtitles[hash]['subid']])
                    # subtitle = self.download_subtitles([subtitles[hash][0]])
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

    for x in range(queue.qsize()):
        video = queue.get_nowait()
        if video['type'] == 'Addic7ed':
            addic7ed_list.append(video)
        else:
            queue.put_nowait(video)

    # if addic7ed_list:
    #     catch_all('Addic7ed', addic7ed_list)

    # time.sleep(0.01)  # To prevent race condition

    opensubs_list = [queue.get_nowait() for x in range(queue.qsize())]
    search = []
    for x in opensubs_list:
        opensubs_dict[x['moviehash']] = x

    if opensubs_dict:
        #     catch_all('OpenSubtitles', opensubs_dict, self.lang)
        sub = OpenSubtitles()
        sub.process(opensubs_dict)
        # print(opensubs_dict)
        # for movie_file in opensubs_dict.values():
        #     movie_file['sublanguageid'] = "english"

        #     search.append(movie_file)

        # counter = 0
        # while search[:500]:

        #     print(search[:500], counter)
        #     print(search)
        #     break
        #     counter += 1
        #     search = search[500:]

        # for i in search:
        #     print(i)


process_queue(_queue)

# search = [{'file_name': 'Scarface.198h3.720p.HDTV.x264.AAC.mkv', 'type': 'OpenSubtitles', 'save_subs_to':
#            'E:\\folder for subtitles\\Scarface (1983)\\Scarface.198h3.720p.HDTV.x264.AAC.srt', 'moviehash': 'd307041a90bf99ee',
#            'moviebytesize': '733901213', 'sublanguageid': 'english'}]


search = [{'file_name': 'The.Gentlemen.2019.720p.WEBRip.x264.AAC-[YTS.MX].mp4', 'type': 'OpenSubtitles', 'save_subs_to':
           'E:\\folder for subtitles\\The.Gentlemen.2019.720p.WEBRip.x264.AAC-[YTS.MX].srt', 'moviehash': '5cae1131c852ddc7', 'moviebytesize': '1090144686',
           'sublanguageid': 'eng'},
          {'file_name': 'A.Beautiful.Day.In.The.Neighborhood.2019.720p.WEBRip.x264.AAC-[YTS.MX].mp4', 'type': 'OpenSubtitles',
           'save_subs_to': 'E:\\folder for subtitles\\A Beautiful Day In The Neighborhood\\A.Beautiful.Day.In.The.Neighborhood.2019.720p.WEBRip.x264.AAC-[YTS.MX].srt',
           'moviehash': 'd0bb8b0e76298b8f', 'moviebytesize': '1047149762', 'sublanguageid': 'eng'}]

search = [{'file_name': 'The.Gentlemen.2019.720p.WEBRip.x264.AAC-[YTS.MX].mp4', 'type': 'OpenSubtitles', 'save_subs_to': 'E:\\movies\\The Gentlemen (2019) [720p] [WEBRip] [YTS.MX]\\The.Gentlemen.2019.720p.WEBRip.x264.AAC-[YTS.MX].srt',
           'moviehash': '5cae1131c852ddc7', 'moviebytesize': '1090144686', 'sublanguageid': 'eng'}]

search = [{'sublanguageid': 'eng', 'moviehash': '6d526f9a9934122e', 'moviebytesize': 1531274243}]

# op = OpenSubtitles()
# op.login()
# print(op._query_opensubs(search))

# results = []


# def clean_results(results, imdb=False):
#     subtitles = {}
#     user_ranks = {'administrator': 1,
#                   'platinum member': 2,
#                   'vip member': 3,
#                   'gold member': 4,
#                   'trusted': 5,
#                   'silver member': 6,
#                   'bronze member': 7,
#                   'sub leecher': 8,
#                   '': 9, }

#     for result in results:
#         if result['SubBad'] != '1':
#             movie_hash = result.get('MovieHash')
#             if not movie_hash:
#                 movie_hash = self.imdbid_to_hash[int(result['IDMovieImdb'])]
#             subid = result['IDSubtitleFile']
#             downcount = int(result['SubDownloadsCnt'])
#             rating = float(result['SubRating'])
#             IDMovieImdb = int(result['IDMovieImdb'])

#             if rating and rating < 8:
#                 # Ignore poorly rated subtitles, while not
#                 # penalizing the ones that haven't yet been rated
#                 continue

#             user_rank = user_ranks[result['UserRank']]

#             if imdb:
#                 cleaned_release_name = clean_name(result['MovieReleaseName'])
#                 file_name = self.moviefiles[movie_hash]['file_name']
#                 cleaned_file_name = clean_name(file_name)
#                 overlap = len(set.intersection(set(cleaned_release_name), set(cleaned_file_name)))
#             else:
#                 overlap = 0

#             subtitles.setdefault(movie_hash, []).append({
#                 'subid': subid,
#                 'downcount': downcount,
#                 'rating': rating,
#                 'user_rank': user_rank,
#                 'overlap': overlap,
#                 'IDMovieImdb': IDMovieImdb
#             })

#             # subtitles.setdefault(movie_hash, []).append((subid, downcount, rating, user_rank))

#    return subtitles


# try:
#     api_url = 'http://api.opensubtitles.org/xml-rpc'
#     server = ServerProxy(api_url, verbose=False)

#     resp = server.LogIn('', '', 'en', 'PySubD v2.0')
#     # resp = server.LogIn('', '', 'en', 'PySubD v1')

#     login_token = resp['token']

#     tempresp = server.SearchSubtitles(login_token, search)
#     # print(tempresp)
#     if tempresp['data']:
#         results.extend(tempresp['data'])

# except Exception as e:
#     print(e, "error")


# print('Logging out...', 'info')
# resp = server.LogOut(login_token)


# subtitles = clean_results(results)


# for hash, matched_files in subtitles.items():
#     for matches in matched_files:
#         print(matches)
