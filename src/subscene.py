from bs4 import BeautifulSoup
import re
import os
from assist_functions import get_proxies, request_with_proxies
import requests
import time
import zipfile


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
            url = first_search_header + \
                re.split(self.movie, self.file_name)[0].replace('.', '-')
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
                # could try getting a fresh set of proxies
                download_pg = request_with_proxies(self.proxies, url)
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
            r = requests.get(
                "http://subscene.com/subtitles/release?q=" + self.file_name)
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
                lin = soup.find_all('a', attrs={'id': 'downloadButton'})[
                    0].get("href")  # multi attribute find
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
