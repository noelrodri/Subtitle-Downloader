import requests
import re
import time
import os
import glob
import zipfile
import hashlib
import json
from bs4 import BeautifulSoup


def get_proxies():
    from lxml.html import fromstring
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr'):
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            # Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies


def request_with_proxies(proxies, url):
    from itertools import cycle
    i = 0
    header = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'   # make dynamic for better results
    }
    while True:
        proxy_pool = cycle(proxies)
        proxy = next(proxy_pool)
        print("Subscene Request #%d" % i)

        try:
            pg = requests.get(url, headers=header, proxies={"http": proxy, "https": proxy})
            if pg.status_code == 200:
                return pg

        except Exception as e:
            print(e)
            print("Skipping. Connnection error")
        i += 1

        if i > len(proxies):
            print("Exhausted proxies")
            return 0


class SubsceneDowlaod:
    def __init__(self, file_list):
        self.file_list = file_list
        self.yts_re = re.compile(r'yts|YIFY', re.I)
        self.movie = re.compile(r'.\d\d\d\d', re.I)

    def download_manager(self):
        self.proxies = get_proxies()               # uncomment
        for file in self.file_list:
            root, extension = os.path.splitext(file)
            self.file_path = os.path.dirname(root) + '\\'
            self.file_name = os.path.basename(root)
            print(self.file_path)
            print(self.file_name)
            self.subscene_downloader()

    def subscene_downloader(self):

        first_search_header = "https://subscene.com/subtitles/"
        subscene_header = "https://subscene.com"

        if self.yts_re.search(self.file_name):
            url = first_search_header + re.split(self.movie, self.file_name)[0].replace('.', '-')
            pg = request_with_proxies(self.proxies, url)
            if pg:
                soup = BeautifulSoup(pg.content, 'lxml')
                a_tag = soup.find_all('a', href=re.compile("english"))
                output = []
                print(pg.content)
                for i in a_tag:
                    if i.find('span', class_="l r positive-icon") and i.find('span', text=(self.yts_re)):
                        output.append(i)

                if len(output) > 1:
                    download_pg_link = output[0].get('href')

                url = subscene_header + download_pg_link
                download_pg = request_with_proxies(self.proxies, url)       # could try getting a fresh set of proxies
                if download_pg:
                    soup = BeautifulSoup(download_pg, 'lxml')
                    download_link = soup.select('.download a[href]')
                    if download_link:
                        url = subscene_header + download_link[0].get('href')
                        subtitle_file = request_with_proxies(self.proxies, url)
                        if subtitle_file:
                            self.subtitle_file_handler(subtitle_file)

                    else:
                        print("could not find download_link")

        else:
            r = requests.get("http://subscene.com/subtitles/release?q=" + self.file_name)
            soup = BeautifulSoup(r.content, "lxml")
            atags = soup.find_all("a")
            href = ""
            for i in range(0, len(atags)):
                spans = atags[i].find_all("span")
                if(len(spans) == 2 and spans[0].get_text().strip() == "english" and spans[1].get_text().strip() == self.file_name):
                    href = atags[i].get("href").strip()
            print(href)
            if(len(href) > 0):
                r = requests.get("http://subscene.com" + href)
                soup = BeautifulSoup(r.content, "lxml")
                lin = soup.find_all('a', attrs={'id': 'downloadButton'})[0].get("href")
                print('this lint', lin)
                r = requests.get("http://subscene.com" + lin)
                self.subtitle_file_handler(r)

    def subtitle_file_handler(self, sub_file):
        language = "english"
        subfile = open(self.file_path + "{}.zip".format(language), 'wb')
        for chunk in sub_file.iter_content(100000):
            subfile.write(chunk)
        subfile.close()
        time.sleep(1)
        zip_ = zipfile.ZipFile(self.file_path + "{}.zip".format(language))
        zip_.extractall(self.file_path)
        zip_.close()
        os.unlink(self.file_path + "{}.zip".format(language))


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
                for file in glob.glob(glob_path + "*" + extension):     # validating video extension
                    if file not in self.output_list:
                        self.output_list.append(file)
        return self.output_list


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
        root, extension = os.path.splitext(file)
        language_code = 'en'
        filename = root + language_code + ".srt"

        if not os.path.exists(filename):
            headers = {'User-Agent': 'SubDB/1.0 (subtitle-downloader/1.0)'}
            url = "http://api.thesubdb.com/?action=download&hash=" + self.get_hash(file) + "&language=" + language_code
            req = requests.get(url, headers=headers)
            if req.status_code == 200:
                with open(filename, "wb") as subtitle:
                    subtitle.write(req.content)
                    print(language_code + " subtitles successfully downloaded for " + file)
                self.completed.append(file)

            elif req.status_code == 404:
                print("file not found")
                self.notfound.append(file)

            else:
                print("Error")


if __name__ == "__main__":
    fil = FileHandler('E:/The Sultan And The Saint (2016) [WEBRip] [720p] [YTS.AM]')
    # sub = Subdub(fil.file_paths())
    # sub.download_manager()
    # sub.completed
    # sub.notfound
    sub = SubsceneDowlaod(fil.file_paths())
    sub.download_manager()


# sub.download_manager()
# # sub.completed
# sub.notfound


# outputlist = ['E:/Citizen Khan\\Citizen Khan - S01 - E01.avi', 'E:/Citizen Khan\\Citizen Khan - S01 - E02.avi', 'E:/Citizen Khan\\Citizen Khan - S01 - E03.avi']
# notcompleted = []


# dictionary = {
#     "output": outputlist,
#     "notcompleted": notcompleted

# }

# json_object = json.dumps(dictionary, indent=4)
# print(json_object)

# data = json.loads(json_object)

# for i in data['output']:
#     print(i)


# print(json_object)
# with open("sample.json", "w") as outfile:
#     outfile.write(json_object)
