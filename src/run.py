import requests
import re
import time
import os
import glob
import json
from subscene import SubsceneDowload
from subdub import Subdub
from opensubtitles import OpenSubtitles
from addic7ed import Addic7ed
from assist_functions import calc_file_hash


class FileHandler:
    VIDEO_EXTENSIONS = [
        ".avi", ".mp4", ".mkv", ".mpg",
        ".mpeg", ".mov", ".rm", ".vob",
        ".wmv", ".flv", ".3gp", ".3g2"
    ]

    def __init__(self, input_path):
        self.input_path = input_path
        self.movie_list = []

    def file_paths(self):
        for folderName, _, filenames in os.walk(self.input_path):
            for filename in filenames:
                root, extension = os.path.splitext(filename)
                if extension in self.VIDEO_EXTENSIONS and not os.path.exists(os.path.join(folderName, root + '.srt')):
                    self.movie_list.append({
                        'file_name': filename,
                        'save_subs_to': os.path.join(folderName, os.path.splitext(filename)[0] + '.srt'),
                        'moviehash': calc_file_hash(os.path.join(folderName, filename)),
                        'moviebytesize': str(os.path.getsize(os.path.join(folderName, filename)))
                    })


if __name__ == "__main__":
    json_path = f'{os.path.dirname(os.path.realpath(__file__))}/subtitle_downloader.json'
    if os.path.isfile(json_path):
        with open(json_path, "r") as outfile:
            subtitle_json = json.load(outfile)

    else:
        subtitle_path = input("Please Enter Path to file containing Movies")
        while True:
            if os.path.exists(subtitle_path):
                break
            else:
                subtitle_path = input(
                    "The entered path was invalid enter path again")

        dictionary = {
            "subtitle_path": subtitle_path,
            "subs_found": [],
            "subs_not_found": []
        }

        with open(json_path, "w") as outfile:
            outfile.write(json.dumps(dictionary, indent=2))
        subtitle_json = dictionary

    fil = FileHandler(subtitle_json['subtitle_path'])
    fil.file_paths()

    for downloader in [Subdub(fil), SubsceneDowload(fil)]:
        downloader.run()
