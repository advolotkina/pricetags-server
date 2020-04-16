from flask import render_template, redirect, url_for
from . import main
from . import pricetags_app
from flask_login import login_required, current_user
from app.models import Permission, PriceTag


@main.route('/')
def index_page():
    return render_template('index.html'), 200


@pricetags_app.route('/')
@login_required
def pricetags_page():
    if current_user.role_id == Permission.OPERATOR:
        return render_template('pricetags.html', pricetags=PriceTag.query.all()), 200
    return redirect(url_for('main.index_page'))


@pricetags_app.route('/add/')
@login_required
def add_new_pricetag():
    if current_user.role_id == Permission.SERVICER:
        return render_template('add_pricetag.html'), 200
    return redirect(url_for('main.index_page'))


@pricetags_app.route('/remove/')
@login_required
def remove_pricetag():
    if current_user.role_id == Permission.SERVICER:
        return render_template('remove_pricetag.html'), 200
    return redirect(url_for('main.index_page'))
