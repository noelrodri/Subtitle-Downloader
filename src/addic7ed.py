from assist_functions import download_url_content
from assist_functions import save_subs
from bs4 import BeautifulSoup
from assist_functions import guess_file_data
from operator import itemgetter
import re
import traceback


class Addic7ed:

    host = 'http://www.addic7ed.com'

    LANGUAGES = {
        u'English': ('1', 'eng'),
        u'French': ('8', 'fre'),
        u'Greek': ('27', 'ell'),
        u'Spanish': ('4', 'spa'),
        u'Portuguese(Br)': ('10', 'pob'),
        u'Italian': ('7', 'ita'),
    }

    def __init__(self, file_list):
        self.files_list = file_list

    def run(self):
        print('Querying Addic7ed.com...', 'info')

        for details_dict in self.files_list:
            filename = details_dict['file_name']
            save_to = details_dict['save_subs_to']

            try:
                searched_url, downloadlink = self._query(filename)
                if downloadlink:
                    subs = self.download_subtitles(
                        searched_url, downloadlink, filename)
                else:
                    print('Nothing found.', 'error')
                    print(details_dict)
                    continue

            except NoInternetConnectionFound:
                print('No active Internet connection found. Kindly check and try again.')

            except:
                for details_dict in self.files_list:
                    print(details_dict, "limit exceeded")
                raise

            else:
                save_subs(subs, save_to)
                self.files_list.remove(details_dict)
        return self.file_list

    def process(self, files_list, lang='English'):
        self.lang = lang
        self.files_list = files_list
        self.run()

    def _query(self, filename):
        print(f'Searching Addic7ed.com for {filename} info')
        guessed_file_data = guess_file_data(filename)
        name = guessed_file_data.get('name')
        season = guessed_file_data.get('season')
        episode = guessed_file_data.get('episode')
        teams = guessed_file_data.get('teams')

        lang_code = self.LANGUAGES[self.lang][0]
        searchurl = f'{self.host}/serie/{name}/{season}/{episode}/{lang_code}'
        print(searchurl)
        name = name.lower().replace(' ', '_')
        teams = set(teams)

        best_match = None

        page_html = download_url_content(searchurl)
        if not page_html.strip():
            return searchurl, None
        soup = BeautifulSoup(page_html, features='lxml')
        release_pattern = re.compile(r'Version (.*),', re.I)
        team_split = re.compile(r'\.| - ')

        try:
            sub_list = soup.find_all(
                'td', {'class': 'NewsTitle', 'align': 'center'})
            result = []

            for subs in sub_list:
                subteams = set(team_split.split(
                    release_pattern.findall(subs.get_text().lower())[0]))

                link = f'http://www.addic7ed.com{subs.parent.parent.select(".buttonDownload")[0].get("href")}'
                b = {}
                b['link'] = link

                if subteams.issubset(teams):
                    b['overlap'] = len(set.intersection(
                        teams, subteams))   # check match of teams
                else:
                    b['overlap'] = 0

                b['download_count'] = int(subs.parent.parent.findAll(
                    'td', {'class': 'newsDate', 'colspan': '2'})[0].get_text().strip().split()[4])

                result.append(b)
        except:
            print('Following unknown exception occured:\n%s' %
                  traceback.format_exc(), 'error')

        else:
            if result:
                best_match = sorted(result, key=itemgetter(
                    'overlap', 'download_count'), reverse=True)[0]

        return (searchurl, best_match.get('link') if best_match else None)

    def download_subtitles(self, searchurl, link, filename):
        referer = searchurl.replace('_', ' ')
        print('Saving subtitles for %s...' % filename, 'success')
        return download_url_content(link, referer)
