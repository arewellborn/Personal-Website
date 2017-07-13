# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""

import re

from flask import flash
from flask_sqlalchemy import BaseQuery
from sqlalchemy.orm import exc
from werkzeug.exceptions import abort


def flash_errors(form, category='warning'):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash('{0} - {1}'.format(getattr(form, field).label.text, error), category)


def get_object_or_404(model, *criterion):
    """Query db or return 404"""
    try:
        if type(model) == BaseQuery:
            return model.filter(*criterion).one()
        else:
            return model.query.filter(*criterion).one()
    except exc.NoResultFound or exc.MultipleResultsFound:
        abort(404)


def slugify(text, delim='-'):
    """Generates a slug."""
    punc = r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+'
    result = []
    for word in re.split(punc, text.lower()):
        if word:
            result.append(word)
    return delim.join(result)
