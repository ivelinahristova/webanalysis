import datetime
import re
from abc import ABC
from typing import Text, Generator


class Scraper(ABC):
    def get_name(self) -> Text:
        pass

    def list_articles(self, soup) -> Generator[Text, None, None]:
        pass

    def get_date(self, soup):
        return datetime.datetime.today()

    def get_author(self, soup) -> Text:
        pass

    def get_content(self, soup) -> Text:
        pass

    def get_sentences_count(self, soup) -> int:
        try:
            text = self.get_clean_content(soup)
            matches = re.findall("[А-Я][^.]+[(\.\s)]", text)
            return len(matches)
        except:
            #@todo: error log
            print('Error while counting sentences')
            return 0

    def get_clean_content(self, soup) -> Text:
        body = self.get_content(soup)
        return self.clean_html(body)

    def clean_html(self, text) -> Text:
        return re.sub('<[^<]+?>|"', '', text)
