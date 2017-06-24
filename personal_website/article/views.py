# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request, url_for, session
from flask_login import login_required, current_user

from .models import Article
from .forms import ArticleForm
from personal_website.utils import flash_errors, get_object_or_404

from flask import Flask
app = Flask(__name__)

blueprint = Blueprint('article', __name__, url_prefix='/blog', static_folder='../static')


@blueprint.route('/')
def blog():
    """List published articles"""

    query = Article.public().order_by(Article.timestamp.desc())
    return render_template('articles/blog_index.html', query=query)


@blueprint.route('/<slug>/', methods=['GET'])
def article(slug):
    """Call Article from slug"""
    if current_user and current_user.is_authenticated:
        article = get_object_or_404(Article, Article.slug == slug)
    else:
        article = get_object_or_404(Article.public(), Article.slug == slug)
    return render_template('articles/article.html', article=article)


@blueprint.route('/drafts/')
@login_required
def drafts():
    """List unpublished articles"""

    query = Article.drafts().order_by(Article.timestamp.desc())
    return render_template('articles/blog_index.html', query=query)



@blueprint.route('/create/', methods=['GET', 'POST'])
@login_required
def create():
    """Create an article"""
    form = ArticleForm(request.form)

    if request.method == 'POST':
        if form.validate_on_submit():
            article = Article.create(title=form.title.data, body=form.body.data, 
                                     published=form.published.data, author=current_user)
            flash('You have created an article', 'success')
            if article.published:
                return redirect(url_for('.article', slug=article.slug))
            else:
                return redirect(url_for('.edit', slug=article.slug))

        else:
            flash_errors(form)
    return render_template('articles/create.html', form=form)


@blueprint.route('/<slug>/edit/', methods=['GET', 'POST'])
@login_required
def edit(slug):
    """Edit an existing article"""
    article = get_object_or_404(Article, Article.slug == slug)

    if request.method == 'POST':
        form = request.form
        app.logger.debug('request form keys = {}'.format(list(form.items())))
        if form.get('title') and form.get('body'):

            if form.get('published'):
                published = True
            else:
                published = False

            article = article.update(title=form['title'], body=form['body'], published=published)
            
            if article.published:
                flash('Article updated and published', 'success')
                return redirect(url_for('.article', slug=article.slug))
            else:
                flash('Article updated', 'success')
                return redirect(url_for('.drafts'))

        else:
            flash('Title and body required.', 'danger')

    return render_template('articles/edit.html', article=article)

