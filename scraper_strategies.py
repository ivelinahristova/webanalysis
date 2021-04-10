from scrapers import Scraper
from typing import AnyStr, Callable
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

class DariknewsStrategy(Scraper):
    def get_name(self) -> AnyStr:
        return 'dariknews'
    def get_list_url(self):
        URL = 'https://dariknews.bg/novini'
        return URL
    def list_articles(self, soup):
        articles = soup.findAll('article', {'itemprop': 'itemListElement'})
        for article in articles:
            header = article.div.div.h2
            if header is not None:
                link = header.a.get('href')
                link = link.replace('//', 'https://')
                print(link)
                yield link
    def get_keywords(self, soup):
        keywords = soup.findAll("a", {"class": "gtm-Tags-click"})
        for keyword in keywords:
            yield keyword.text.strip()
    def get_date(self, soup):
        tag = soup.find('time', {'itemprop': 'datePublished'})
        if tag:
            date = tag['datetime']
            res = re.match(r"^(?P<y>\d{4})-(?P<m>\d{2})-(?P<d>\d{2})\s+(?P<H>\d{2}):(?P<M>\d{2}):(?P<S>\d{2})", date)
            y = int(res.group('y'))
            m = int(res.group('m'))
            d = int(res.group('d'))
            H = int(res.group('H'))
            M = int(res.group('M'))
            S = int(res.group('S'))

            date = datetime.datetime(y, m, d, H, M, S)
        else:
            return super(DariknewsStrategy, self).get_date(soup)

        return date

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

class BivolStrategy(Scraper):
    def get_name(self) -> AnyStr:
        return 'bivol'

    def get_list_url(self):
        URL = 'https://bivol.bg/'
        return URL

    def list_articles(self, soup):
        articles = soup.findAll('article')
        for article in articles:
            a = article.find('a')
            if a is not None:
                link = a.get('href')
                print(link)
                yield link

    def get_keywords(self, soup):
        keywords = soup.findAll("a", {"rel": "tag"})
        for keyword in keywords:
            yield keyword.text.strip()
    def get_date(self, soup):
        meta = soup.find('meta', {'property': 'article:published_time'})
        if meta:
            date = soup.find('meta', {'property': 'article:published_time'})['content']
            date = date[0:-6]
            date = date.replace('T', ' ')
            res = re.match(r"^(?P<y>\d{4})-(?P<m>\d{2})-(?P<d>\d{2})\s+(?P<H>\d{2}):(?P<M>\d{2}):(?P<S>\d{2})", date)
            y = int(res.group('y'))
            m = int(res.group('m'))
            d = int(res.group('d'))
            H = int(res.group('H'))
            M = int(res.group('M'))
            S = int(res.group('S'))

            date = datetime.datetime(y, m, d, H, M, S)
        else:
            return super(BivolStrategy, self).get_date(soup)

        return date
