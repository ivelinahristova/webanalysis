from abc import ABC
import re
import datetime
import sys

class Scraper(ABC):
    def get_name(self):
        pass
    def list_articles(self, soup):
        pass
    def get_date(self, soup):
        return datetime.datetime.today()
    def get_author(self, soup):
        pass
    def get_content(self, soup):
        pass
    def get_sentences_count(self, soup):
        try:
            text = self.get_clean_content(soup)
            matches = re.findall("[А-Я][^.]+[(\.\s)]", text)
            return len(matches)
        except:
            #@todo: error log
            print('Error while counting sentences')
            return 0
    def get_clean_content(self, soup):
        body = self.get_content(soup)
        return self.clean_html(body)
    def clean_html(self, text):
        return re.sub('<[^<]+?>|"', '', text)
