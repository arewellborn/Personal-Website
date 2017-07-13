# -*- coding: utf-8 -*-
"""Article model."""

import datetime as dt

from flask import Markup
from markdown import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.extra import ExtraExtension
from micawber import bootstrap_basic, parse_html
from micawber.cache import Cache as OEmbedCache

from personal_website.database import db, Column, Model, SurrogatePK, reference_col
from personal_website.utils import slugify


class Article(SurrogatePK, Model):
    """The articles a user creates."""

    __tablename__ = 'articles'
    title = Column(db.String(32), unique=True, nullable=False)
    body = Column(db.String(2048))
    published = Column(db.Boolean(), default=False)
    timestamp = Column(db.DateTime, default=dt.datetime.now(), nullable=False)
    slug = Column(db.String(48), unique=True, nullable=False)
    user_id = reference_col('users')

    def __init__(self, title, body, **kwargs):
        """Initialize Article."""
        Model.__init__(self, title=title, body=body, **kwargs)
        if self.title:
            self.slug = slugify(self.title)
        else:
            self.slug = self.id

    @classmethod
    def public(cls):
        """Return published articles."""
        return Article.query.filter_by(published=True)

    @classmethod
    def drafts(cls):
        """Return Draft articles."""
        return Article.query.filter_by(published=False)

    @property
    def html_content(self):
        """Parse article bosy for markup and features."""
        hilite = CodeHiliteExtension(linenums=False, css_class='highlight')
        extras = ExtraExtension()
        markdown_content = markdown(self.body, extensions=[hilite, extras])
        oembed_providers = bootstrap_basic(OEmbedCache)
        oembed_content = parse_html(
            markdown_content,
            oembed_providers,
            urlize_all=True)
        return Markup(oembed_content)

    def __repr__(self):
        """Represent instance as a unique string"""
        return '<Article({slug})>'.format(slug=self.slug)
