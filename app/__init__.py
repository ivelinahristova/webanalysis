"""
    webanalysis
    ~~~~~~~~~~~~~~~~~~
    webanalysis is a project to extract and analyse web-related data.
    It delivers human-readable conclusions via API.
"""

import datetime
import os
import re
import pandas as pd
import matplotlib.pyplot as plt
from pprint import pprint
from typing import AnyStr, Text

import click
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from flask import Flask

from app import utils
from app.api import api
from app.db import db
from app.frontend import frontend
from app.models import Article, Keyword, Author
from proxies.proxies import Proxies
from scrapers.scraper_resolver import ScraperResolver

load_dotenv()

app = Flask(__name__)
app.config.from_pyfile('../config.py')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_CONN')

app.register_blueprint(api)
app.register_blueprint(frontend)

with app.app_context():
    db.init_app(app)


@app.cli.command('plot-share-charts')
@click.argument('month')  # In format 2021-03
def plot_share_charts(month: Text) -> None:
    sources = ScraperResolver().get_all()
    for source in sources:
        plot_shares(source, month)


def plot_shares(source, month='2021-03'):
    from_date = datetime.datetime.strptime(f'{month}-01', '%Y-%m-%d')
    to_date = from_date + datetime.timedelta(weeks=4)

    query = db.session.query(Article).filter(
        Article.shares_count >= 0,
        (Article.date > from_date),
        (Article.date < to_date),
        Article.source == source
    )
    if query.count == 0:
        return
    df = pd.read_sql(query.statement, db.session.bind)
    plt.figure()

    df['date'] = df['date'].apply(lambda x: x.day)
    if df.empty:
        return
    df = df.groupby('date').agg({'shares_count': 'mean'})
    df.reset_index(inplace=True)
    plt.plot(df['date'], df['shares_count'], marker='o',
             markerfacecolor='skyblue', markersize=12, color='skyblue',
             linewidth=4)

    plt.savefig(f'export/{month}_{source}.png')


@app.cli.command('fetch-shares')
def fetch_db_shares() -> None:
    query = db.session.query(Article).filter(Article.shares_count is None)
    for article in query.limit(100).all():
        url = article.url
        shares_count = get_fb_shares(url)
        article.shares_count = shares_count
        db.session.add(article)
        db.session.commit()


def get_fb_shares(url: Text) -> int:
    api_key = os.environ.get('SHARED_COUNT_KEY')
    sc_url = 'https://api.sharedcount.com/v1.0/'
    params = {'url': url, 'apiKey': api_key}
    content = requests.get(sc_url, params=params)
    fb_data = content.json()['Facebook']
    return fb_data['share_count']


@app.cli.command('scrape-web')
@click.argument('name')
def scrape(name: AnyStr):
    with app.app_context():
        resolver = ScraperResolver()
        scraper = resolver.get_strategy(name)
        source = scraper.get_name()
        url = scraper.get_list_url()
        proxy_resolver = Proxies()

        page = get_request(url, proxy_resolver)
        soup = BeautifulSoup(page.content, 'html.parser')
        for link in scraper.list_articles(soup):
            if re.search('^https', link):
                scrape_article(link, source, scraper, proxy_resolver)


def scrape_article(url: AnyStr, source: AnyStr, scraper, proxy_resolver):
    """
    :param scraper
    :param url: AnyStr
    :param connection:
    :param source: AnyStr
    """
    page = get_request(url, proxy_resolver)
    soup = BeautifulSoup(page.content, 'lxml')
    article_title = soup.title.text
    date = scraper.get_date(soup)
    author = scraper.get_author(soup)
    sentence_count = scraper.get_sentences_count(soup)
    author_obj = False
    if author:
        author_obj = create_author(author, source)
        db.session.add(author_obj)
        db.session.commit()

    article = create_article(article_title, source, url, date, sentence_count)
    if article:
        for keyword in scraper.get_keywords(soup):
            keyword_obj = create_keyword(keyword)
            pprint(keyword_obj)
            if keyword_obj:
                article.keywords.append(keyword_obj)
                res = db.session.add(article)
                db.session.commit()
            if author_obj:
                article.author = author_obj.id
                db.session.add(article)
                db.session.commit()


def create_article(title: AnyStr, source: AnyStr, url: AnyStr,
                   date: datetime, sentence_count: int):
    """

    :param title:
    :param source:
    :param cursor:
    :return:
    """
    title = utils.clean_data(title)
    source = utils.clean_data(source)
    url = utils.clean_data(url)
    date = date.strftime('%Y-%m-%d %H:%M:%S')
    article = False
    query = db.session.query(Article).filter(Article.url == url)
    if query.count() == 0:
        article = Article(title, source, date, url, sentence_count)
        res = db.session.add(article)
        db.session.commit()

    return article


def create_keyword(title):
    title = utils.clean_data(title)
    print(title)
    print('create_keyword')
    keyword = False
    query = db.session.query(Keyword).filter(Keyword.title == title)
    if query.count() == 0:
        keyword = Keyword(title)
        res = db.session.add(keyword)
        db.session.commit()
    else:
        keyword = query.first()

    return keyword


def create_author(title, source):
    title = utils.clean_data(title)
    print(title)
    print('create_author')
    author = False
    query = db.session.query(Author).filter(Author.title == title,
                                            Author.source == source)
    if query.count() == 0:
        author = Author(title, source)
        db.session.add(author)
        db.session.commit()
    else:
        author = query.first()

    return author


def get_request(url, proxy_resolver):
    content = ''
    try:
        proxy = proxy_resolver.get_proxy()
        if proxy:
            user_agent = proxy_resolver.get_user_agent()
            headers = {'user-agent': user_agent}

            proxies = {}
            if app.config['USE_PROXY']:
                proxies = {'http': proxy, 'https': proxy}
            content = requests.get(url, headers=headers,
                                   proxies=proxies, timeout=10)
        else:
            raise Exception('Proxy was not resolved properly')
    except Exception as e:
        print(f'error {e}')
        print('..next proxy..')
        proxy_resolver.next_proxy()
        return get_request(url, proxy_resolver)

    return content

