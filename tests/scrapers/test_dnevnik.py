import datetime
import os

from bs4 import BeautifulSoup

from scrapers.scraper_strategies.dnevnik_strategy import DnevnikStrategy


class TestDnevnikScraper:
    file = 'data/asset_d.html'

    def init(self):
        self.scraper = DnevnikStrategy()

    def test_get_content(self):
        self.init()
        dir = os.path.dirname(__file__)
        soup = BeautifulSoup(
            open(f'{dir}/{self.file}', encoding='utf8'),
            'lxml')
        content = self.scraper.get_content(soup)
        assert isinstance(content, str)

    def test_sentences_count(self):
        self.init()
        dir = os.path.dirname(__file__)
        soup = BeautifulSoup(
            open(f'{dir}/{self.file}', encoding='utf8'),
            'lxml')
        count = self.scraper.get_sentences_count(soup)
        assert count == 21

    def test_get_author(self):
        self.init()
        dir = os.path.dirname(__file__)
        soup = BeautifulSoup(
            open(f'{dir}/{self.file}', encoding='utf8'),
            'lxml')
        author = self.scraper.get_author(soup)
        assert author == 'Author John'

    def test_get_date(self):
        self.init()
        dir = os.path.dirname(__file__)
        soup = BeautifulSoup(
            open(f'{dir}/{self.file}', encoding='utf8'),
            'lxml')
        date = self.scraper.get_date(soup)
        assert date == datetime.datetime.today()
