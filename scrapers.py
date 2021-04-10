from abc import ABC, abstractmethod
from typing import AnyStr, Callable
from pprint import pprint
import datetime

class Scraper(ABC):
    def get_name(self):
        pass
    def list_articles(self, soup):
        pass
    def get_date(self, soup):
        return datetime.datetime.today()
