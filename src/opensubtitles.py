from collections import Counter
from xmlrpc.client import ServerProxy
import base64
import zlib
from assist_functions import save_subs


class OpenSubtitles:

    api_url = 'http://api.opensubtitles.org/xml-rpc'
    login_token = None
    server = None

    LANGUAGES = {
        u'English': ('1', 'eng'),
        u'French': ('8', 'fre'),
        u'Greek': ('27', 'ell'),
        u'Spanish': ('4', 'spa'),
        u'Portuguese(Br)': ('10', 'pob'),
        u'Italian': ('7', 'ita'),
    }

    def __init__(self, parent=None):
        self.stopping = False

    def process(self, files_list, lang='English'):
        self.moviefiles = files_list
        self.imdbid_to_hash = {}
        self.lang = self.LANGUAGES[lang][1]
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

        self.server = ServerProxy(self.api_url)

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

                    tempresp = self.server.SearchSubtitles(
                        self.login_token, search[:500])

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

    def clean_results(self, results):
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

                    movie_hash = self.imdbid_to_hash[int(
                        result['IDMovieImdb'])]

                subid = result['IDSubtitleFile']
                downcount = int(result['SubDownloadsCnt'])
                rating = float(result['SubRating'])
                IDMovieImdb = int(result.get('IDMovieImdb', 0))

                if rating and rating < 8:
                    # Ignore poorly rated subtitles, while not
                    # penalizing the ones that haven't yet been rated
                    continue

                user_rank = user_ranks[result['UserRank']]

                subtitles.setdefault(movie_hash, []).append(
                    (subid, downcount, rating, user_rank, IDMovieImdb))

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
                cnt[dicts[4]] += 1

            most_common = cnt.most_common(1)[0][0]
            expectedResult = [d for d in found_matches if d[4] == most_common]
            print(expectedResult, "expected")

            subtitles[hash] = sorted(
                found_matches, key=lambda x: (x[3], -x[2], -x[1]))[0]

        for (hash, filedetails) in self.moviefiles.items():
            if not self.stopping:
                if subtitles.get(hash):

                    print('Saving subtitles for %s' %
                          filedetails['file_name'], 'success')
                    subtitle = self.download_subtitles([subtitles[hash][0]])
                    save_subs(
                        subtitle, filedetails['save_subs_to'], subtitles[hash])

                else:
                    print("no sub found")
            else:
                return

    def download_subtitles(self, subparam):
        resp = self.server.DownloadSubtitles(self.login_token, subparam)
        self.check_status(resp)
        decoded = base64.standard_b64decode(
            resp['data'][0]['data'].encode('ascii'))

        decompressed = zlib.decompress(decoded, 15 + 32)
        return decompressed
