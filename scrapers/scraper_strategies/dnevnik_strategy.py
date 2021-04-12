from scrapers.scrapers import Scraper
from typing import AnyStr
import datetime
import re


class DnevnikStrategy(Scraper):
    def get_name(self) -> AnyStr:
        return 'dnevnik'
    def get_list_url(self):
        URL = 'https://www.dnevnik.bg/allnews/today/'
        return URL
    def list_articles(self, soup):
        content = soup.findAll('div', {'class': 'grid-container'})
        articles = soup.findAll("article")
        for article in articles:
            header = article.div.h2
            if header is not None:
                link = header.a.get('href')
                print(link)
                yield link
    def get_keywords(self, soup):
        keywords = soup.findAll("li", {"itemprop": "keywords"})
        for keyword in keywords:
            yield keyword.text.strip()
    def get_date(self, soup):
        meta = soup.find('meta', {'property': 'article:published_time'})
        if meta:
            date = meta['content']
            res = re.match(r"^(?P<y>\d{4})-(?P<m>\d{2})-(?P<d>\d{2})", date)
            y = int(res.group('y'))
            m = int(res.group('m'))
            d = int(res.group('d'))

            date = datetime.datetime(y, m, d, 0, 0, 0)
        else:
            return super(DnevnikStrategy, self).get_date(soup)

        return date
    def get_author(self, soup):
        span = soup.find('span', {'itemprop': 'author'})
        if span:
            meta = span.find('meta', {'itemprop': 'name'})
            return meta['content'].strip()

        return False