from flask import Flask
import click
from pprint import pprint
import requests
from bs4 import BeautifulSoup
from typing import AnyStr
import re
from scrapers.scraper_resolver import ScraperResolver
from proxies.proxies import Proxies
import datetime
from app.db import db
from app.models import Article, Keyword
import os
from dotenv import load_dotenv
from app import utils
from app.api import api
from app.frontend import frontend

load_dotenv()

app = Flask(__name__)
app.config.from_pyfile('../config.py')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_CONN")

app.register_blueprint(api)
app.register_blueprint(frontend)

with app.app_context():
    db.init_app(app)


@app.cli.command("scrape-web")
@click.argument("name")
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
            if re.search("^https", link):
                scrape_article(link, source, scraper, proxy_resolver)


def scrape_article(url: AnyStr, source: AnyStr, scraper, proxy_resolver):
    """
    :param scraper
    :param url: AnyStr
    :param connection:
    :param source: AnyStr
    """
    page = get_request(url, proxy_resolver)
    soup = BeautifulSoup(page.content, 'html.parser')
    article_title = soup.title.text
    date = scraper.get_date(soup)
    article = create_article(article_title, source, url, date)
    if article:
        for keyword in scraper.get_keywords(soup):
            keyword_obj = create_keyword(keyword)
            pprint(keyword_obj)
            if keyword_obj:
                article.keywords.append(keyword_obj)
                res = db.session.add(article)
                db.session.commit()


def create_article(title: AnyStr, source: AnyStr, url: AnyStr, date: datetime):
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
        article = Article(title, source, date, url)
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


def get_request(url, proxy_resolver):
    content = ''
    try:
        proxy = proxy_resolver.get_proxy()
        if proxy:
            user_agent = proxy_resolver.get_user_agent()
            headers = {'user-agent': user_agent}

            proxies = {}
            if app.config['USE_PROXY']:
                proxies = {"http": proxy, "https": proxy}
            content = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        else:
            pass #@todo: throw exception
    except:
        print('error')
        proxy_resolver.next_proxy()
        return get_request(url, proxy_resolver)

    pprint(content)
    return content

