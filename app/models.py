from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from typing import Text

from app.db import db

Base = declarative_base()

articles_keywords = db.Table(
    'article_keyword',
    db.Column('article_id', db.Integer,
              db.ForeignKey('articles.id', ondelete='CASCADE'),
              nullable=False),
    db.Column('keyword_id', db.Integer,
              db.ForeignKey('keywords.id', ondelete='CASCADE'),
              nullable=False)
)


class Article(db.Model):

    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    source = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    url = db.Column(db.String(255), nullable=False)
    author = Column(Integer, ForeignKey("authors.id"))
    sentences_count = db.Column(db.Integer)
    keywords = db.relationship(
        'Keyword',
        secondary=articles_keywords,
        primaryjoin=(articles_keywords.c.article_id == id),
        backref=db.backref('articles', lazy='dynamic'),
        lazy='dynamic'
    )

    def __init__(self, title, source, date, url, sentences_count) -> None:
        self.title = title
        self.source = source
        self.date = date
        self.url = url
        self.sentences_count = sentences_count

    def __repr__(self) -> Text:
        return '<title {}'.format(self.title)


class Keyword(db.Model):

    __tablename__ = 'keywords'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)

    def __init__(self, title) -> None:
        self.title = title

    def __repr__(self) -> Text:
        return 'Keyword, title {}'.format(self.title)


class Author(db.Model):

    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    source = db.Column(db.String(255), nullable=False)

    def __init__(self, title, source) -> None:
        self.title = title
        self.source = source

    def __repr__(self) -> Text:
        return 'Author, title {}'.format(self.title)
