from scrapers.scrapers import Scraper
from typing import AnyStr
import datetime
import re


class VestiStrategy(Scraper):
    def get_name(self) -> AnyStr:
        return 'vesti'

    def get_list_url(self):
        URL = 'https://www.vesti.bg/posledni-novini'
        return URL

    def list_articles(self, soup):
        articles = soup.findAll('div', {'class': 'list-item list-item-category'})
        for article in articles:
            header = article.figure.find('div', {'class': 'text-holder'}).figcaption.h2
            if header is not None:
                link = header.a.get('href')
                print(link)
                yield link

    def get_keywords(self, soup):
        keywords = soup.findAll("a", {"itemprop": "keywords"})
        for keyword in keywords:
            yield keyword.text.strip()

    def get_date(self, soup):
        tag = soup.find('time', {'itemprop': 'datePublished'})
        if tag:
            date = tag['datetime']
            res = re.match(r"^(?P<d>\d{2}).(?P<m>\d{2}).(?P<y>\d{4})", date)
            y = int(res.group('y'))
            m = int(res.group('m'))
            d = int(res.group('d'))

            date = datetime.datetime(y, m, d, 0, 0, 0)
        else:
            return super(VestiStrategy, self).get_date(soup)

        return date
    def get_author(self, soup):
        div = soup.find('h3', {'class': 'author'})
        if div:
            span = div.find('span')
            if span:
                a = span.find('a')
                return a.text.strip()

        return False