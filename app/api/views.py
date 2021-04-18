from flask import (
    Blueprint,
    Response
)
from app import utils, db
import datetime
from scrapers.scraper_resolver import ScraperResolver
import json
from sqlalchemy import text

api = Blueprint('api', __name__)

@api.route('/sources')
def sources():
    resolver = ScraperResolver()
    sources = resolver.get_all().keys()

    response = Response(json.dumps(list(sources)), mimetype='application/json')
    return response

@api.route('/keywords/', defaults={'name': None})
@api.route('/keywords/<name>')
def keywords(name):
    source = False
    if name:
        source = utils.clean_data(name)
    today = datetime.date.today().isoformat()
    # today = '2021-04-08 00:00:00' #@todo: fix
    if source:
        sql = text(f'select keywords.id as id, count(keywords.id) as counts, \
                    keywords.title from article_keyword as ak \
                    left join articles on ak.article_id = articles.id \
                    left join keywords on ak.keyword_id = keywords.id \
                    where date > {today!r} and source = {source!r} \
                    group by keywords.id having counts > 1')
        result = db.session.execute(sql)
    else:
        sql = text(f'select keywords.id as id, count(keywords.id) as counts, \
                    keywords.title from article_keyword as ak \
                    left join articles on ak.article_id = articles.id \
                    left join keywords on ak.keyword_id = keywords.id \
                    where date > {today!r} \
                    group by keywords.id having counts > 1')
        result = db.session.execute(sql)

    all_articles = [dict(r._mapping.items()) for r in result]

    response = Response(json.dumps(all_articles), mimetype='application/json')
    return response
