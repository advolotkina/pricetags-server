from flask import render_template, redirect, url_for, flash, send_from_directory
from . import main
from . import pricetags_app
from flask_login import login_required, current_user
from app.models import Permission, PriceTag, Good, PriceTagToGood
from .forms import AddPriceTagForm, RemovePriceTagForm
from app import db
from pricetag_update import upload_data_to_pricetag


@main.route('/')
def index_page():
    return render_template('index.html'), 200


@main.route('/images/<path:path>')
def send_image(path):
    """Метод для тестирования загрузки изображений и файлов с "удалённого" сервера"""
    return send_from_directory('/home/zhblnd/diplom/flask-server/images', path)


@pricetags_app.route('/')
@login_required
def pricetags_page():
    if current_user.role_id == Permission.OPERATOR:
        return render_template('pricetags.html', pricetags=PriceTag.query.all()), 200
    return redirect(url_for('main.index_page'))


@pricetags_app.route('/add/', methods=['GET', 'POST'])
@login_required
def add_new_pricetag():
    form = AddPriceTagForm()
    form.goods.choices = [(good.id, good.name) for good in Good.query.all()]
    if form.validate_on_submit():
        pricetag = PriceTag.query.filter_by(serial_number=form.serial.data).first()
        if pricetag is None:
            try:
                new_pricetag = PriceTag(form.serial.data)
                db.session.add(new_pricetag)
                db.session.flush()

                goods = form.goods.data
                index = 1
                for good in goods:
                    new_pricetag_to_good = PriceTagToGood(index, new_pricetag.id, good)
                    db.session.add(new_pricetag_to_good)
                    index += 1
                db.session.commit()
                redirect(url_for('pricetags_app.add_new_pricetag'))
            except Exception:
                db.session.rollback()
            else:
                # print('no errors')
                upload_data_to_pricetag(form.serial.data)
        else:
            flash('Ценник с таким серийным номером уже существует.')
    if current_user.role_id == Permission.SERVICER:
        return render_template('add_pricetag.html', form=form), 200
    return redirect(url_for('main.index_page'))


@pricetags_app.route('/remove/', methods=['GET', 'POST'])
@login_required
def remove_pricetag():
    form = RemovePriceTagForm()
    form.pricetags.choices = [(pricetag.id, pricetag.serial_number) for pricetag in PriceTag.query.all()]
    if form.validate_on_submit():
        try:
            for pricetag_id in form.pricetags.data:
                PriceTag.query.filter_by(id=pricetag_id).delete()
                PriceTagToGood.query.filter_by(pricetag_id=pricetag_id).delete()
            db.session.commit()
            redirect(url_for('pricetags_app.remove_pricetag'))
        except Exception:
            db.session.rollback()
    if current_user.role_id == Permission.SERVICER:
        return render_template('remove_pricetag.html', form=form), 200
    return redirect(url_for('main.index_page'))
