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
from bs4 import BeautifulSoup
import traceback
import requests
import socket
from operator import itemgetter

LANGUAGES = {
    u'English': ('1', 'eng'),
    u'French': ('8', 'fre'),
    u'Greek': ('27', 'ell'),
    u'Spanish': ('4', 'spa'),
    u'Portuguese(Br)': ('10', 'pob'),
    u'Italian': ('7', 'ita'),
}


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


class NoInternetConnectionFound(Exception):
    pass


class IncorrectResponseRecieved(Exception):
    pass


class DailyDownloadLimitExceeded(Exception):
    pass


request_headers = {
    'Host': 'www.addic7ed.com',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:14.0) Gecko/20100101 Firefox/14.0.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-us,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
}


def download_url_content(url, referer=None, timeout=10):
    ''' Downloads and returns the contents of the given url.'''

    if referer:
        request_headers['Referer'] = referer
    else:
        request_headers['Referer'] = url

    try:
        x = requests.get(url, headers=request_headers, timeout=timeout)
    except (requests.exceptions.Timeout, exceptions.ConnectionError, socket.timeout):
        raise NoInternetConnectionFound

    if x.status_code != 200:
        raise IncorrectResponseRecieved

    # print(x.content)
    # if x.content.find('Daily Download count exceeded') != -1:
    #     raise DailyDownloadLimitExceeded
    # else:
    return x.content


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


def save_subs(content, full_path, other_details=None):
    open(full_path, 'wb').write(content)


class Addic7ed:

    host = 'http://www.addic7ed.com'

    def __init__(self, parent=None):
        self.stopping = False

    def run(self):
        print('Querying Addic7ed.com...', 'info')
        for details_dict in self.files_list[:]:
            if not self.stopping:
                filename = details_dict['file_name']
                save_to = details_dict['save_subs_to']

                try:
                    (searched_url, downloadlink) = self._query(filename)
                    if downloadlink:
                        subs = self.download_subtitles(searched_url, downloadlink, filename)
                    else:
                        print('Nothing found.', 'error')
                        print(details_dict)
                        continue

                except NoInternetConnectionFound:
                    print('No active Internet connection found. Kindly check and try again.', 'error')
                except:  # utils.DailyDownloadLimitExceeded:
                    for details_dict in self.files_list:
                        (details_dict)
                    raise
                else:
                    save_subs(subs, save_to)
                    self.files_list.remove(details_dict)

    def process(self, files_list, lang='English'):
        '''Given filename and the wished language, searches and downloads the best match found from Addic7ed.com'''
        self.lang = lang
        self.files_list = files_list
        if not self.stopping:
            self.run()

    def stopTask(self):
        self.stopping = True

    def _listTeams(self, subteams, separators):
        for sep in separators:
            subteams = self._splitTeam(subteams, sep)
        return set(subteams)

    def _splitTeam(self, subteams, sep):
        teams = []
        for t in subteams:
            teams += t.split(sep)
        return teams

    def _query(self, filename):
        print('Searching Addic7ed.com for %s' % filename, 'info')
        guessed_file_data = guess_file_data(filename)
        name = guessed_file_data.get('name')
        season = guessed_file_data.get('season')
        episode = guessed_file_data.get('episode')
        teams = guessed_file_data.get('teams')

        lang_url = LANGUAGES[self.lang][0]
        searchurl = '%s/serie/%s/%s/%s/%s' % (self.host, name, season, episode, lang_url)

        name = name.lower().replace(' ', '_')
        teams = set(teams)

        best_match = None

        page_html = download_url_content(searchurl)
        if not page_html.strip():
            return (searchurl, None)
        soup = BeautifulSoup(page_html, features='lxml')
        release_pattern = re.compile('Version (.+), ([0-9]+).([0-9])+ MBs')

        try:
            sub_list = soup.findAll('td', {'class': 'NewsTitle', 'colspan': '3'})
            result = []

            for subs in sub_list:
                subteams = release_pattern.match(subs.contents[1].strip()).groups()[0].lower()
                subteams = self._listTeams([subteams], ['.', '_', ' '])
                langs_html = subs.find_next('td', {'class': 'language'})
                statusTD = langs_html.find_next('td')
                status = statusTD.text.strip()
                links = statusTD.find_next('td').find_all('a')
                link = '%s%s' % ('http://www.addic7ed.com', links[len(links) - 1]['href'])

                b = {}
                b['link'] = link

                if status == 'Completed':
                    b['completed'] = 1
                    sub_quality = subs.parent.parent.find_all('a', {'class': 'buttonDownload'})[0].text
                    if sub_quality == u'original' or sub_quality == u'most updated':
                        b['best_match'] = 1
                    else:
                        b['best_match'] = 0
                else:
                    b['completed'] = 0

                if subteams.issubset(teams):
                    b['overlap'] = len(set.intersection(teams, subteams))
                else:
                    b['overlap'] = 0
                result.append(b)
        except:
            print('Following unknown exception occured:\n%s' % traceback.format_exc(), 'error')

        else:
            if result:
                # Sort the results found by completed, overlapping, best_match

                best_match = sorted(result, key=itemgetter('completed', 'overlap', 'best_match'), reverse=True)[0]

        return (searchurl, best_match.get('link') if best_match else None)

    def download_subtitles(self, searchurl, link, filename):
        referer = searchurl.replace('_', ' ')
        print('Saving subtitles for %s...' % filename, 'success')
        return download_url_content(link, referer)


def process_queue(queue):
    addic7ed_list = []
    opensubs_dict = {}

    for video in queue:
        if video['type'] == 'Addic7ed':
            addic7ed_list.append(video)

    if addic7ed_list:
        ad = Addic7ed()
        ad.process(addic7ed_list)

    # time.sleep(0.01)  # To prevent race condition

    # for video in queue:
    #     if video['type'] == 'OpenSubtitles':
    #         opensubs_dict[video['moviehash']] = video

    # print(opensubs_dict)
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


input_path = "E:\\Citizen.Khan.S04E01.HDTV.x264-TLA[ettv]"

check_and_add(file_paths(input_path))


process_queue(movie_queue)
