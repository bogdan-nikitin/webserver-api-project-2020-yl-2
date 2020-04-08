"""Модуль со всеми формами приложения."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email
from modules.named_flask_form_field import named_flask_form_field as named_field


class LoginForm(FlaskForm):
    """Форма входа."""
    username = named_field(StringField)('Email')
    password = named_field(PasswordField)('Пароль')
    remember_me = BooleanField('Запомнить меня', default=True)
    submit = SubmitField('Войти')

