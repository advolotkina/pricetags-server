from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Length


class AddPriceTagForm(FlaskForm):
    serial = StringField('Серийный номер', validators=[DataRequired(message='Введите серийный номер'), Length(1, 64)])
    goods = SelectMultipleField('Выберите товары, которые будут отображаться на ценнике',
                                validators=[DataRequired(message='Необходимо выбрать хотя бы один товар для отображения')],
                                coerce=int)
    submit = SubmitField('Добавить ценник')


class RemovePriceTagForm(FlaskForm):
    pricetags = SelectMultipleField('Выберите ценники, которые необходимо убрать',
                                    validators=[DataRequired()], coerce=int)
    submit = SubmitField('Убрать')
