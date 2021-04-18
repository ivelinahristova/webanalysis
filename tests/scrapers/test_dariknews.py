from scrapers.scraper_strategies.dariknews_strategy import DariknewsStrategy
from bs4 import BeautifulSoup
import os

class TestDarikScraper:
    file = 'data/asset_dn.html'

    def init(self):
        self.scraper = DariknewsStrategy()

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
        assert count == 8
