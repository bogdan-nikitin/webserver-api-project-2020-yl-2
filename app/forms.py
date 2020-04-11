"""Модуль со всеми формами приложения."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

from modules.named_flask_form_field import named_flask_form_field as named_field


class LoginForm(FlaskForm):
    """Форма входа в приложение."""
    email = named_field(StringField)('Email')
    password = named_field(PasswordField)('Пароль')
    remember_me = BooleanField('Запомнить меня', default=True)
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    """Форма регистрации в приложении."""
    first_name = named_field(StringField)('Имя', validators=[DataRequired()])
    second_name = named_field(StringField)('Фамилия',
                                           validators=[DataRequired()])
    email = named_field(StringField)('Email',
                                     validators=[DataRequired(), Email()])
    password = named_field(PasswordField)('Пароль', validators=[DataRequired()])
    repeat_password = named_field(PasswordField)(
        'Повторите пароль', validators=[EqualTo('password')]
    )
    submit = SubmitField('Зарегестрироваться')
