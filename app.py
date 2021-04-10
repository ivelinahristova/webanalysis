from flask import Flask
import click
from pprint import pprint
from flask import render_template
import requests
from bs4 import BeautifulSoup
import json
import mariadb
from typing import AnyStr, Callable
import re
from scraper_resolver import ScraperResolver
import time
from proxies import Proxies
import json
import datetime
from db import db
from models import Article, Keyword
from sqlalchemy import text
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_CONN")

with app.app_context():
    db.init_app(app)


@app.route('/')
def media_stats():
    return render_template('media-stats.html')

@app.route('/sources')
def sources():
    resolver = ScraperResolver()
    sources = resolver.get_all().keys()

    response = app.response_class(
        response=json.dumps(list(sources)),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/keywords/', defaults={'name': None})
@app.route('/keywords/<name>')
def keywords(name):
    source = False
    if name:
        source = clean_data(name)
    today = datetime.date.today().isoformat()
    # today = '2021-04-08 00:00:00' #@todo: fix
    if source:
        sql = text(f'select keywords.id as id, count(keywords.id) as counts, keywords.title from article_keyword \
left join articles on article_keyword.article_id = articles.id \
left join keywords on article_keyword.keyword_id = keywords.id where date > {today!r} and source = {source!r} group by keywords.id having counts > 1')
        result = db.session.execute(sql)
    else:
        sql = text(f'select keywords.id as id, count(keywords.id) as counts, keywords.title from article_keyword \
        left join articles on article_keyword.article_id = articles.id \
        left join keywords on article_keyword.keyword_id = keywords.id where date > {today!r} group by keywords.id having counts > 1')
        result = db.session.execute(sql)

    all_articles = [dict(r._mapping.items()) for r in result]

    response = app.response_class(
        response=json.dumps(all_articles),
        status=200,
        mimetype='application/json'
    )
    return response


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
    title = clean_data(title)
    source = clean_data(source)
    url = clean_data(url)
    date = date.strftime('%Y-%m-%d %H:%M:%S')
    article = False
    query = db.session.query(Article).filter(Article.url == url)
    if query.count() == 0:
        article = Article(title, source, date, url)
        res = db.session.add(article)
        db.session.commit()

    return article



def create_keyword(title):
    title = clean_data(title)
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


def clean_data(text):
    return text.replace('"', '&quot;').replace("'", '&quot;')

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

