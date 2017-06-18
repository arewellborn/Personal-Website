# -*- coding: utf-8 -*-
"""Article model"""
import datetime as dt
import re
from micawber import parse_html
from micawber.cache import Cache as OEmbedCache
from markdown import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.extra import ExtraExtension
from flask import Markup

from personal_website.database import Column, Model, SurrogatePK, db, reference_col, relationship


class Article(SurrogatePK, Model):
    """The aritcles a user creates"""
    
    __tablename__ = 'articles'
    title = Column(db.String(32), unique=True, nullable=False)
    body = Column(db.String(2048))
    published = Column(db.Boolean(), default=False)
    timestamp = Column(db.DateTime, default=dt.datetime.now(), nullable=False)
    slug = Column(Column(db.String(48), unique=True, nullable=False)
    user_id = reference_col('users', nullable=False)
    user = relationship('User', backref='articles')

    def __init__(self, title, body, **kwargs):
        Model.__init__(title=title, body=body, **kwargs)
        if self.title:
            self.slug = slugify(self.title)
        else:
            self.slug = self.id

    def slugify(self, text, delim='-'):
        """Generates a slug."""
        punc = r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+'
        result = []
        for word in re.split(punc, text.lower()):
            if word:
                result.append(word)
        return delim.join(result)

    @classmethod
    def pubilc(cls):
        return Article.filter_by(published=True)

    @classmethod
    def drafts(cls):
        return Article.filter_by(published=False)

    @property
    def html_content(self):
        hilite = CodeHiliteExtension(linenums=False, css_class='highlight')
        extras = ExtraExtension()
        markdown_content = markdown(self.body, extensions=[hilite, extras])
        oembed_content = parse_html(
            markdown_content,
            oembend_providers,
            urlize_all=True)
        return Markup(oembed_content)

    def __repr__(self):
        """Represent instance as a unique string"""
        return '<{slug}>'.format(slug=self.slug)
