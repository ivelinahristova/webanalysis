from app.db import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

articles_keywords = db.Table(
    'article_keyword',
    db.Column('article_id', db.Integer,
              db.ForeignKey('articles.id', ondelete="CASCADE"),
              nullable=False),
    db.Column('keyword_id', db.Integer,
              db.ForeignKey('keywords.id', ondelete="CASCADE"),
              nullable=False)
)


class Article(db.Model):

    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    source = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    url = db.Column(db.String(255), nullable=False)
    # keywords = db.relationship('Keyword', secondary='ArticleKeyword')
    keywords = db.relationship(
        "Keyword",
        secondary=articles_keywords,
        primaryjoin=(articles_keywords.c.article_id == id),
        backref=db.backref("articles", lazy="dynamic"),
        lazy="dynamic"
    )

    def __init__(self, title, source, date, url):
        self.title = title
        self.source = source
        self.date = date
        self.url = url

    def __repr__(self):
        return '<title {}'.format(self.title)


class Keyword(db.Model):

    __tablename__ = "keywords"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    # articles = db.relationship(Article, secondary='ArticleKeyword')

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<title {}'.format(self.title)


# class ArticleKeyword(db.Model):
#
#     __tablename__ = 'article_keyword'
#
#     article_id = db.Column(
#       Integer,
#       ForeignKey('articles.id'),
#       primary_key=True)
#
#     keyword_id = db.Column(
#        Integer,
#        ForeignKey('keywords.id'),
#        primary_key=True)