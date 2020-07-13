import os
import struct
from lxml.html import fromstring
import requests
import re

request_headers = {
    'Host': 'www.addic7ed.com',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:14.0) Gecko/20100101 Firefox/14.0.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-us,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
}

tv_show_regex = re.compile(
    r"(?:[^\\]\\)*(?P<SeriesName>.*) S?(?P<SeasonNumber>[0-9]+)(?:[ .XE]+(?P<EpisodeNumber>[0-9]+))(?P<Teams>.*)", re.IGNORECASE)

movie_regex = re.compile(
    '(?P<movie>.*)[\.|\[|\(| ]{1}(?P<year>(?:(?:19|20)[0-9]{2}))(?P<teams>.*)', re.IGNORECASE)


def get_proxies():

    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr'):
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            # Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0],
                              i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies


def request_with_proxies(proxies, url):
    from itertools import cycle
    i = 0
    header = {
        # make dynamic for better results
        "User-Agent": 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
    }
    while True:
        proxy_pool = cycle(proxies)
        proxy = next(proxy_pool)
        print("Subscene Request #%d" % i)

        try:
            pg = requests.get(url, headers=header, proxies={
                              "http": proxy, "https": proxy})
            if pg.status_code == 200:
                return pg

        except Exception as e:
            print(e)
            print("Skipping. Connnection error")
        i += 1

        if i > len(proxies):
            print("Exhausted proxies")
            return 0


def is_video_file(filename):
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


def unicode(arg):
    return str(arg)


def clean_name(name):
    name = re.sub('[\W_]+', ' ', unicode(name.lower()))
    name = re.sub(r"\s+", ' ', name)
    return name


def download_url_content(url, referer=None, timeout=10):
    ''' Downloads and returns the contents of the given url.'''

    if referer:
        request_headers['Referer'] = referer
    else:
        request_headers['Referer'] = url

    try:
        x = requests.get(url, headers=request_headers, timeout=timeout)
    except Exception as e:
        print(e)
        raise e

    if x.status_code != 200:
        raise Exception("Invalid Response From Server")

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
