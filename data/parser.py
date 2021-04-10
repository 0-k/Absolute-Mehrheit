from bs4 import BeautifulSoup
import requests
from config.config import config
from src.party import Party


class Parser:

    def __init__(self):
        self.soup = None
        self.__query_latest()

    @staticmethod
    def __query_latest():
        r = requests.get(config['poll_url'])
        file = open('polls_cashed.html', "w")
        file.write(r.text)
        file.close()

    def __make_soup(self):
        with open('polls_cashed.html') as fp:
            self.soup = BeautifulSoup(fp, 'html.parser')

    def get_latest_polls_of(self, party):
        if self.soup is None:
            self.__make_soup()
        return self.soup.find(id=party.id).find_all("td")


if __name__ == '__main__':
    parser = Parser()
    union = Party(name='UNION', id='cdu')
    percentages = parser.get_latest_polls_of(union)
    for percentage in percentages[1:9]:
        print(float(percentage.text.split(' ')[0].replace(',', '.')))
