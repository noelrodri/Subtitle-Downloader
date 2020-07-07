import os
import hashlib
import requests


class Subdub:
    def __init__(self, file_list):
        self.file_list = file_list
        self.completed = []
        self.notfound = []

    def download_manager(self):
        for file in self.file_list:
            self.get_from_subdb(file)

    def get_hash(self, file):
        read_size = 64 * 1024
        with open(file, 'rb') as f:
            data = f.read(read_size)
            f.seek(-read_size, os.SEEK_END)
            data += f.read(read_size)
        return hashlib.md5(data).hexdigest()

    def get_from_subdb(self, file):
        root, _ = os.path.splitext(file)
        language_code = 'en'
        filename = root + language_code + ".srt"

        if not os.path.exists(filename):
            headers = {'User-Agent': 'SubDB/1.0 (subtitle-downloader/1.0)'}
            url = "http://api.thesubdb.com/?action=download&hash=" + \
                self.get_hash(file) + "&language=" + language_code
            req = requests.get(url, headers=headers)
            if req.status_code == 200:
                with open(filename, "wb") as subtitle:
                    subtitle.write(req.content)
                    print(language_code +
                          " subtitles successfully downloaded for " + file)
                self.completed.append(file)

            elif req.status_code == 404:
                print("file not found")
                self.notfound.append(file)

            else:
                print("Error")
