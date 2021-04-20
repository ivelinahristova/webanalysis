import datetime
import json

from flask import Blueprint, Response
from sqlalchemy import text
from typing import Text

from app import utils
from app.db import db
from scrapers.scraper_resolver import ScraperResolver

api = Blueprint('api', __name__)


@api.route('/sources')
def sources() -> Response:
    resolver = ScraperResolver()
    sources = resolver.get_all().keys()

    response = Response(json.dumps(list(sources)), mimetype='application/json')
    return response


@api.route('/keywords/', defaults={'name': None})
@api.route('/keywords/<name>')
def keywords(name: Text) -> Response:
    source = False
    if name:
        source = utils.clean_data(name)
    month_ago = (datetime.date.today() - datetime.timedelta(days=30)).isoformat()
    # today = '2021-04-08 00:00:00' #@todo: fix

    if source:
        sql = text(f'select keywords.id as id, count(keywords.id) as counts, \
                    keywords.title from article_keyword as ak \
                    left join articles on ak.article_id = articles.id \
                    left join keywords on ak.keyword_id = keywords.id \
                    where date > {month_ago!r} and source = {source!r} \
                    group by keywords.id having counts > 1')
        result = db.session.execute(sql)
    else:
        sql = text(f'select keywords.id as id, count(keywords.id) as counts, \
                    keywords.title from article_keyword as ak \
                    left join articles on ak.article_id = articles.id \
                    left join keywords on ak.keyword_id = keywords.id \
                    where date > {month_ago!r} \
                    group by keywords.id having counts > 1')
        result = db.session.execute(sql)

    all_articles = [dict(r._mapping.items()) for r in result]

    response = Response(json.dumps(all_articles), mimetype='application/json')
    return response
