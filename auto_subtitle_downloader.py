import requests
import re
import time
import os
import glob
import json
from subscene import SubsceneDowlaod
from subdub import Subdub
from opensubtitles import OpenSubtitles
from addic7ed import Addic7ed


class FileHandler:
    def __init__(self, input_path):
        self.input_path = input_path
        self.file_list = []
        self.output_list = []
        self.VIDEO_EXTENSIONS = [
            ".avi", ".mp4", ".mkv", ".mpg",
            ".mpeg", ".mov", ".rm", ".vob",
            ".wmv", ".flv", ".3gp", ".3g2"
        ]

    def file_paths(self):
        for folderName, subfolders, filenames in os.walk(self.input_path):
            for filename in filenames:
                path = folderName + '\\' + filename
                self.file_list.append(path)

        for i in self.file_list:
            glob_path = glob.escape(i.rsplit('\\', 1)[0]) + '\\'
            for extension in self.VIDEO_EXTENSIONS:
                # validating video extension
                for file in glob.glob(glob_path + "*" + extension):
                    if file not in self.output_list:
                        self.output_list.append(file)
        return self.output_list


if __name__ == "__main__":

    json_path = f'{os.path.dirname(os.path.realpath(__file__))}/subtitle_downloader.json'
    if os.path.isfile(json_path):
        with open(json_path, "r") as outfile:
            subtitle_json = json.load(outfile)

    else:
        subtitle_path = input("Please Enter Path to file containing Movies")
        dictionary = {
            "subtitle_path": subtitle_path,
            "subs_found": [],
            "subs_not_found": []
        }

        with open(json_path, "w") as outfile:
            outfile.write(json.dumps(dictionary, indent=2))

    print(subtitle_json['subtitle_path'])
    # fil = FileHandler(subtitle_json['subtitle_path'])
    fil = FileHandler('home/noel/Videos/auto_subtitles')

    print(fil.file_paths())

    # sub = SubsceneDowlaod(fil.file_paths())
    # sub.download_manager()
    # sub = Subdub(fil.file_paths())
    # sub.download_manager()
    # sub.completed
    # sub.notfound
