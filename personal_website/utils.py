# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from flask import flash
from sqlalchemy.orm import exc
from werkzeug.exceptions import abort

def flash_errors(form, category='warning'):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash('{0} - {1}'.format(getattr(form, field).label.text, error), category)

def get_object_or_404(model, *criterion):
    try:
        return model.query.filter(*criterion).one()
    except exc.NoResultFound or exc.MultipleResultsFound:
        abort(404)
