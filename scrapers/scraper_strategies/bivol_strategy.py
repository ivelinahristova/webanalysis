import datetime
import re
from typing import AnyStr

from scrapers.scrapers import Scraper


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
        keywords = soup.findAll('a', {'rel': 'tag'})
        for keyword in keywords:
            yield keyword.text.strip()
    def get_date(self, soup):
        meta = soup.find('meta', {'property': 'article:published_time'})
        if meta:
            date = soup.find('meta',
                             {'property': 'article:published_time'})['content']
            date = date[0:-6]
            date = date.replace('T', ' ')
            regex = r"""
            ^(?P<y>\d{4})-(?P<m>\d{2})-(?P<d>\d{2})\s+
            (?P<H>\d{2}):(?P<M>\d{2}):(?P<S>\d{2})
            """
            res = re.match(regex, date, re.VERBOSE)
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
    def get_author(self, soup):
        span = soup.find('span', {'class': 'author vcard'})
        if span:
            a = span.find('a')
            return a.text.strip()

        return False
    def get_content(self, soup):
        body = soup.find('div', {'itemprop': 'articleBody'})
        return body.text.strip()
