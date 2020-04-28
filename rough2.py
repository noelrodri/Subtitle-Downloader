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


default_words = ["i do not understand", "i love you man", "can you win the premeir league for Arsenal?", "fucking kikes man", "hahah", "fucking liverpool man",
                 "hows the weather?", "how are you guys holding up", "why cant i see anything", "why did you betray the motherland man", "9/11", "moses and friends",
                 "A computer makes as many mistakes in one second as three men working for thirty years straight"]

# import time
# from bs4 import BeautifulSoup
# from selenium import webdriver


# emoji_menu = driver.find_element_by_xpath("//button[@class='_1x_c3 _35Ob4 kQJNA _2-5II _338za']")
# laughing = driver.find_element_by_xpath("//div[@class='M6HbS']/span[@data-emoji-index='6']")
# emoji_exit = driver.find_element_by_xpath("//button[@class='_1x_c3 _35Ob4 _12JTM _2WGh-']").click()
# send_btn = driver.find_element_by_xpath('//footer//div[@class="weEq5"][2]').click()

def abhimanyu():
    while True:
        soup = latest_soup()
        message = soup.select('div[class~=Tkt2p]')[-1]
        if message.findAll("div", {"data-pre-plain-text": abhimanyu_name}):
            msg_box = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
            msg_box.send_keys("fucking brilliant abhimanyu")
            emoji_menu = driver.find_element_by_xpath("//button[@class='_1x_c3 _35Ob4 kQJNA _2-5II _338za']")
            emoji_menu.click()
            laughing = driver.find_elements_by_xpath("//div[@class='M6HbS']/span[@data-emoji-index='6']")[-3]
            for i in range(4):
                time.sleep(2)
                laughing.click()
            click_button()
            # driver.find_element_by_xpath("//button[@class='_1x_c3 _35Ob4 _12JTM _2WGh-']").click()
        time.sleep(15)


class WhatsappReplies:
    def __init__(self, driver):
        import re
        from itertools import cycle
        self.reply_pool = cycle(default_words)
        self.driver = driver
        self.msg_box = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        self.soup = None
        self.name = re.compile(r"nöel")
        self.abhimanyu = re.compile(r"abhimanyu", re.I)

    def click_button(self):
        driver.find_element_by_xpath('//footer//div[@class="weEq5"][2]').click()

    def conv_starter(self):
        start_time = time.time()
        self.msg_box.send_keys("hellow")
        self.click_button()
        while True:
            if time.time() - start_time >= 300:
                self.msg_box.send_keys("hellow")
                self.click_button()
                self.latest_soup()
                message = self.soup.select('div[class~=Tkt2p]')[-1]
                my_minutes, my_meridian = self.get_minutes(message.select('span[class~=_3EFt_]'))

            name = self.get_name(my_minutes, my_meridian)
            if name:
                reply = "hi" + str(name)
                self.msg_box.send_keys(reply)
                break
            time.sleep(30)

    def get_name(self, my_minutes, my_meridian):
        self.latest_soup()
        messages = self.soup.select('div[class~=Tkt2p]')[-4:]
        for div in reversed(messages):
            name = div.select('div[class~=_111ze] > span')
            if name:
                minutes, meridian = self.get_minutes(div.select('span[class~=_3EFt_]'))
                if minutes > my_minutes and meridian >= my_meridian:
                    return name

        return 0

    def get_minutes(self, time):
        time = time[0].get_text()
        time, meridian = time.split(' ')
        hour, minutes = time.split(':')
        total = int(hour) + int(minutes) * 60
        return total, meridian

    def latest_soup(self):
        html = self.driver.page_source
        self.soup = BeautifulSoup(html)

    def get_text(self):
        self.latest_soup()
        message = self.soup.select('div[class~=Tkt2p]')[-1]
        if not message.findAll("div", {"data-pre-plain-text": self.name}):
            text = message.select('div[class~=_3zb-j] span span')[0].get_text()
            return text

    def conversation(self):
        keys = self.word_dictionary.keys()
        while True:
            text = self.get_text()
            if text:
                for key in keys:
                    if key in text:
                        reply = word_dictionary[key]

                if not reply:
                    for i in text.split:
                        if i in word_dictionary:
                            reply = word_dictionary[i]

                reply = next(self.reply_pool)
                self.msg_box.send_keys(reply)
                self.click_button()

        # if reply == 'hi':
        #     reply == 'hi' + str(get_name())

        # else:
        #     reply = next(reply_pool)


subtitles = {'6d526f9a9934122e': [{'subid': '1956257637', 'downcount': 1001119, 'rating': 10.0, 'user_rank': 1, 'overlap': 0},
                                  {'subid': '1956306563', 'downcount': 1668761, 'rating': 0.0, 'user_rank': 1, 'overlap': 0},
                                  {'subid': '1956418101', 'downcount': 555189, 'rating': 10.0, 'user_rank': 1, 'overlap': 0},
                                  {'subid': '1956418099', 'downcount': 148443, 'rating': 10.0, 'user_rank': 1, 'overlap': 0},
                                  {'subid': '1956419288', 'downcount': 257621, 'rating': 10.0, 'user_rank': 1, 'overlap': 0},
                                  {'subid': '1956419226', 'downcount': 153813, 'rating': 10.0, 'user_rank': 5, 'overlap': 0},
                                  {'subid': '1956414348', 'downcount': 135510, 'rating': 10.0, 'user_rank': 1, 'overlap': 0},
                                  {'subid': '1956407595', 'downcount': 103133, 'rating': 0.0, 'user_rank': 1, 'overlap': 0},
                                  {'subid': '1956407594', 'downcount': 53721, 'rating': 0.0, 'user_rank': 1, 'overlap': 0},
                                  {'subid': '1956013517', 'downcount': 50037, 'rating': 10.0, 'user_rank': 5, 'overlap': 0},
                                  {'subid': '1956407596', 'downcount': 18631, 'rating': 0.0, 'user_rank': 1, 'overlap': 0},
                                  {'subid': '1956407597', 'downcount': 11616, 'rating': 0.0, 'user_rank': 1, 'overlap': 0},
                                  {'subid': '1956308389', 'downcount': 113596, 'rating': 10.0, 'user_rank': 2, 'overlap': 0},
                                  {'subid': '1956418531', 'downcount': 64646, 'rating': 0.0, 'user_rank': 2, 'overlap': 0},
                                  {'subid': '1956110721', 'downcount': 17825, 'rating': 0.0, 'user_rank': 2, 'overlap': 0},
                                  {'subid': '1956426598', 'downcount': 15536, 'rating': 0.0, 'user_rank': 4, 'overlap': 0},
                                  {'subid': '1956339431', 'downcount': 171000, 'rating': 0.0, 'user_rank': 7, 'overlap': 0},
                                  {'subid': '1955499849', 'downcount': 17733, 'rating': 0.0, 'user_rank': 7, 'overlap': 0},
                                  {'subid': '1953783096', 'downcount': 34745, 'rating': 0.0, 'user_rank': 9, 'overlap': 0},
                                  {'subid': '1956423125', 'downcount': 32971, 'rating': 0.0, 'user_rank': 9, 'overlap': 0}]}


subtitles1 = {'6d526f9a9934122e': [
    ('1956306563', 1668761, 0.0, 1),
    ('1956418101', 555189, 10.0, 1),
    ('1956418099', 148443, 10.0, 1),
    ('1956419288', 257621, 10.0, 1),
    ('1956419226', 153813, 10.0, 5),
    ('1956414348', 135510, 10.0, 1),
    ('1956407595', 103133, 0.0, 1),
    ('1956407594', 53721, 0.0, 1),
    ('1956013517', 50037, 10.0, 5),
    ('1956407596', 18631, 0.0, 1),
    ('1956407597', 11616, 0.0, 1),
    ('1956257637', 1001119, 10.0, 1),
    ('1956308389', 113596, 10.0, 2),
    ('1956418531', 64646, 0.0, 2),
    ('1956110721', 17825, 0.0, 2),
    ('1956426598', 15536, 0.0, 4),
    ('1956339431', 171000, 0.0, 7),
    ('1955499849', 17733, 0.0, 7),
    ('1953783096', 34745, 0.0, 9),
    ('1956423125', 32971, 0.0, 9)]}


subtitles2 = [{'subid': '1956257637', 'downcount': 1006125, 'rating': 10.0, 'user_rank': 1, 'overlap': 0, 'IDMovieImdb': 4154664},
              {'subid': '1956418101', 'downcount': 563766, 'rating': 10.0, 'user_rank': 1, 'overlap': 0, 'IDMovieImdb': 4154796},
              {'subid': '1956418099', 'downcount': 149932, 'rating': 10.0, 'user_rank': 1, 'overlap': 0, 'IDMovieImdb': 4154796},
              {'subid': '1956419288', 'downcount': 261164, 'rating': 10.0, 'user_rank': 1, 'overlap': 0, 'IDMovieImdb': 4154796},
              {'subid': '1956419226', 'downcount': 156838, 'rating': 10.0, 'user_rank': 5, 'overlap': 0, 'IDMovieImdb': 4154796},
              {'subid': '1956414348', 'downcount': 137156, 'rating': 10.0, 'user_rank': 1, 'overlap': 0, 'IDMovieImdb': 4154796},
              {'subid': '1956407595', 'downcount': 103616, 'rating': 0.0, 'user_rank': 1, 'overlap': 0, 'IDMovieImdb': 4154796},
              {'subid': '1956407594', 'downcount': 54041, 'rating': 0.0, 'user_rank': 1, 'overlap': 0, 'IDMovieImdb': 4154796},
              {'subid': '1956013517', 'downcount': 50339, 'rating': 10.0, 'user_rank': 5, 'overlap': 0, 'IDMovieImdb': 4154756},
              {'subid': '1956407596', 'downcount': 18806, 'rating': 0.0, 'user_rank': 1, 'overlap': 0, 'IDMovieImdb': 4154796},
              {'subid': '1956407597', 'downcount': 11737, 'rating': 0.0, 'user_rank': 1, 'overlap': 0, 'IDMovieImdb': 4154796},
              {'subid': '1956308389', 'downcount': 113939, 'rating': 10.0, 'user_rank': 2, 'overlap': 0, 'IDMovieImdb': 4154796},
              {'subid': '1956418531', 'downcount': 65334, 'rating': 0.0, 'user_rank': 2, 'overlap': 0, 'IDMovieImdb': 4154796},
              {'subid': '1956110721', 'downcount': 18083, 'rating': 0.0, 'user_rank': 2, 'overlap': 0, 'IDMovieImdb': 5764096},
              {'subid': '1956426598', 'downcount': 15688, 'rating': 0.0, 'user_rank': 4, 'overlap': 0, 'IDMovieImdb': 4154796},
              {'subid': '1956339431', 'downcount': 171336, 'rating': 0.0, 'user_rank': 7, 'overlap': 0, 'IDMovieImdb': 4154796},
              {'subid': '1955499849', 'downcount': 17951, 'rating': 0.0, 'user_rank': 7, 'overlap': 0, 'IDMovieImdb': 5998104},
              {'subid': '1953783096', 'downcount': 35010, 'rating': 0.0, 'user_rank': 9, 'overlap': 0, 'IDMovieImdb': 583487},
              {'subid': '1956423125', 'downcount': 33472, 'rating': 0.0, 'user_rank': 9, 'overlap': 0, 'IDMovieImdb': 4154796}
              ]


# x = subtitles1['6d526f9a9934122e']

# for zeta in sorted(x, key=lambda y: (y[3], -y[2], -y[1])):

#     print(zeta)

subtitle3 = {}

from collections import Counter
cnt = Counter()

for varriables in subtitle3:
    cnt[varriables['IDMovieImdb']] += 1

# most_common = cnt.most_common(1)[0][0]
print(cnt.most_common(2))
# expectedResult = [d for d in subtitles2 if d['IDMovieImdb'] == most_common]

# for i in expectedResult:
#     print(i)


from operator import itemgetter as i
from functools import cmp_to_key


def multikeysort(items, columns):
    comparers = [((i(col[1:].strip()), -1) if col.startswith('-') else (i(col.strip()), 1)) for col in columns]

    def cmp(a, b):
        return (a > b) - (a < b)

    def comparer(left, right):
        comparer_iter = (cmp(fn(left), fn(right)) * mult for fn, mult in comparers)
        return next((result for result in comparer_iter if result), 0)

    return sorted(items, key=cmp_to_key(comparer))


# for (hash, found_matches) in subtitles.items():
#     #     # print(found_matches)
#     print(multikeysort(found_matches, ['overlap', 'user_rank', '-rating', '-downcount'])[0])
    #         print(dicts)
    # print(sorted(found_matches, key=i('overlap', 'user_rank', 'rating', 'downcount'))[0])

    # print(found_matches)

    # for dict_list in subtitles.values():
    #     x = sorted(dict_list, key=i('overlap', 'user_rank', 'downcount'))

    # def compare_function(dicts):
    #     if dicts["user_rank"] == 1:
    #         return True

    #     else:
    #         False

    # def compare_function2(dicts):
    #     if dicts["rating"] >= 10:
    #         return True

    #     else:
    #         False

    # hitler = sorted(filter(compare_function, x), key=i('rating'), reverse=True)

    # hitler = sorted(filter(compare_function2, hitler), key=i('downcount'), reverse=True)

    # for zeta in hitler:
    #     print(zeta)

    # print(hitler[0])

    # for zeta in filter(compare_function, x):
    #     print(zeta)

    # hitler = sorted(hitler, key=i('downcount'))

    # print(hitler[0])
