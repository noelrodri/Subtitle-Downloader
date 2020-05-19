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


tv_show_regex = re.compile(r"(?:[^\\]\\)*(?P<SeriesName>.*) S?(?P<SeasonNumber>[0-9]+)(?:[ .XE]+(?P<EpisodeNumber>[0-9]+))(?P<Teams>.*)", re.I)


movie_regex = re.compile('(?P<movie>.*)[\.|\[|\(| ]{1}(?P<year>(?:(?:19|20)[0-9]{2}))(?P<teams>.*)', re.IGNORECASE)


request_headers = {
    'Host': 'www.addic7ed.com',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:14.0) Gecko/20100101 Firefox/14.0.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-us,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
}

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
