import requests
import os.path
import datetime as dt
from bs4 import BeautifulSoup

from config.config import config
import src.parties as parties


class Loader:

    def __init__(self):
        self.soup = None
        self.__query_latest()
        self.__make_soup()

    def __query_latest(self):
        if self.__has_already_been_cached_today():
            return
        else:
            self.__make_request()

    def __has_already_been_cached_today(self):
        if self.__cache_did_change_today():
            return True
        return False

    def __cache_did_change_today(self):
        if self.__cache_does_not_exist():
            return False
        today = dt.datetime.now().date()
        filetime = dt.datetime.fromtimestamp(os.path.getctime(config['caching_filename']))
        return filetime.date() == today

    def __cache_does_not_exist(self):
        return not os.path.exists(config['caching_filename'])

    def __make_request(self):
        r = requests.get(config['poll_url'])
        file = open(config['caching_filename'], "w")
        file.write(r.text)
        file.close()

    def __make_soup(self):
        with open(config['caching_filename']) as fp:
            self.soup = BeautifulSoup(fp, 'html.parser')

    def get_latest_percentages_of(self, party):
        soup = self.__filter_soup(party.id)
        percentages = [float(item.text.split(' ')[0].replace(',', '.')) for item in soup]
        return percentages

    def __filter_soup(self, id):
        return self.soup.find(id=id).find_all("td")[1:9]

    def get_latest_dates_of_polls(self):
        soup = self.__filter_soup('datum')
        dates = [dt.datetime.strptime(item.text, '%d.%m.%Y').date() for item in soup]
        return dates


if __name__ == '__main__':
    parser = Loader()
    percentages = parser.get_latest_percentages_of(parties.GRUENE)
    dates = parser.get_latest_dates_of_polls()
