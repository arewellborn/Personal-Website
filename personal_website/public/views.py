# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from personal_website.extensions import login_manager
from personal_website.public.forms import LoginForm
from personal_website.user.forms import RegisterForm
from personal_website.user.models import User
from personal_website.utils import flash_errors

blueprint = Blueprint('public', __name__, static_folder='../static')


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route('/')
def home():
    """Home page."""
    return render_template('public/home.html')


@blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    """Login."""
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash('You are logged in.', 'success')
            return form.redirect('user.members')

        else:
            flash_errors(form)
    return render_template('public/login.html', form=form)


@blueprint.route('/logout/')
@login_required
def logout():
    """Logout."""
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))


@blueprint.route('/about/')
def about():
    """About page."""
    return render_template('public/about.html')
