import datetime
from typing import Text

import click

from flask import Blueprint

from app.db import db
from app.models import Article
from app.social.social_data_extractor import SocialDataExtractor
from app.social.plotter import Plotter
from scrapers.scraper_resolver import ScraperResolver

social = Blueprint('social', __name__)


@social.cli.command('plot-shares')
@click.argument('month')  # In format 2021-03
def plot_share_charts(month: Text) -> None:
    sources = ScraperResolver().get_all()
    for source in sources:
        plot_shares(source, month)


def plot_shares(source, month='2021-03'):
    from_date = datetime.datetime.strptime(f'{month}-01', '%Y-%m-%d')
    to_date = from_date + datetime.timedelta(weeks=4)
    plotter = Plotter()
    plotter.plot_share_counts(from_date, to_date, source, month)


@social.cli.command('fetch-shares')
def fetch_db_shares() -> None:
    extractor = SocialDataExtractor()
    query = db.session.query(Article).filter(Article.shares_count == None)
    for article in query.limit(100).all():
        url = article.url
        shares_count = extractor.get_fb_shares(url)
        article.shares_count = shares_count
        db.session.add(article)
        db.session.commit()

