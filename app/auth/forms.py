from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message='Введите e-mail'), Length(1, 64), Email(message='Невалидный e-mail')])
    password = PasswordField('Пароль', validators=[DataRequired(message='Введите пароль')])
    remember_me = BooleanField('Оставаться в системе')
    submit = SubmitField('Войти')
