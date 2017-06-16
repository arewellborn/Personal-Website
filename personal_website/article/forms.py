# -*- coding: utf-8 -*-
"""Article forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length
from flask import request

from .models import Article


class ArticleForm(FlaskForm):
    """Article form."""

    title = StringField('title',
                        validators=[DataRequired()])
    body = StringField('body')
    published = BooleanField('published')

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super().__init__(*args, **kwargs)

    def validate(self):
        """Validate the form."""
        initial_validation = super().validate()
        if not initial_validation:
            return False
        title = Article.query.filter_by(title=self.title.data).first()
        if title:
            self.title.errors.append('Title already Used')
            return False
        slug = Article.query.filter_by(slug=self.slug.data).first()
        if slug:
            self.title.errors.append('Error producing url. Try a different title.')
            return False
        return True

