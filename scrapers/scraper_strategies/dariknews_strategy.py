import datetime
import re
from typing import AnyStr

from scrapers.scrapers import Scraper


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
        keywords = soup.findAll('a', {'class': 'gtm-Tags-click'})
        for keyword in keywords:
            yield keyword.text.strip()

    def get_date(self, soup):
        tag = soup.find('time', {'itemprop': 'datePublished'})
        if tag:
            date = tag['datetime']
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
            return super(DariknewsStrategy, self).get_date(soup)

        return date

    def get_author(self, soup):
        div = soup.find('div', {'itemprop': 'author'})
        if div:
            span = div.find('span', {'itemprop': 'name'})
            return span.text.strip()

        return False

    def get_content(self, soup):
        body = soup.find('div', {'itemprop': 'articleBody text'})
        div = body.find('div', {'class': 'on-topic'})
        if div:
            div.decompose()
        return body.text.strip()
