"""Модуль со всеми формами приложения."""

import phonenumbers
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField,
                     IntegerField, FileField, TextAreaField)
from wtforms.validators import (DataRequired, Email, EqualTo, ValidationError,
                                NumberRange, Optional)

from modules.named_flask_form_field import named_flask_form_field as named_field

FIELD_MUST_BE_FILLED_IN = 'Это поле необходимо заполнить'
SPECIFY_VALID_EMAIL = 'Укажите действительный адрес электронной почты'
SPECIFY_VALID_AGE = 'Укажите действительный возраст'
PASSWORDS_DO_NOT_MATCH = 'Пароли не совпадают'


class PhoneNumber:
    """Валидатор для проверки номера телефона."""

    def __init__(self, *, message='Указан недействительный номер'):
        self.message = message

    def __call__(self, form, field):
        try:
            number = phonenumbers.parse(field.data)
            if not phonenumbers.is_valid_number(number):
                raise ValidationError(self.message)
        except phonenumbers.NumberParseException:
            raise ValidationError(self.message)


class LoginForm(FlaskForm):
    """Форма входа в приложение."""
    email = named_field(StringField)('Email')
    password = named_field(PasswordField)('Пароль')
    remember_me = BooleanField('Запомнить меня', default=True)
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    """Форма регистрации в приложении."""
    first_name = named_field(StringField)(
        'Имя', validators=[DataRequired(FIELD_MUST_BE_FILLED_IN)])
    second_name = named_field(StringField)(
        'Фамилия', validators=[DataRequired(FIELD_MUST_BE_FILLED_IN)])
    email = named_field(StringField)(
        'Email', validators=[DataRequired(FIELD_MUST_BE_FILLED_IN),
                             Email(SPECIFY_VALID_EMAIL)])
    password = named_field(PasswordField)(
        'Пароль', validators=[DataRequired(FIELD_MUST_BE_FILLED_IN)])
    repeat_password = named_field(PasswordField)(
        'Повторите пароль', validators=[
            EqualTo('password', PASSWORDS_DO_NOT_MATCH)]
    )
    submit = SubmitField('Зарегестрироваться')


class ChangeProfileInfoForm(FlaskForm):
    """Форма изменения профиля."""
    first_name = named_field(StringField)('Имя')
    second_name = named_field(StringField)('Фамилия')
    phone_number = named_field(StringField)('Номер телефона',
                                            validators=[Optional(),
                                                        PhoneNumber()])
    age = named_field(IntegerField)(
        'Возраст', validators=[Optional(),
                               NumberRange(1, message=SPECIFY_VALID_AGE)]
    )
    city = named_field(StringField)('Город')
    additional_inf = named_field(TextAreaField)('Дополнительная информация')
    avatar = named_field(FileField)('Аватар')

    submit = SubmitField('Сохранить изменения')


class ChangeProfileSecurityForm(FlaskForm):
    email = named_field(StringField)(
        'Email', validators=[Optional(), Email(SPECIFY_VALID_EMAIL)])
    old_password = named_field(PasswordField)('Старый пароль',
                                              validators=[Optional()])
    password = named_field(PasswordField)(
        'Пароль', validators=[Optional(),
                              DataRequired(FIELD_MUST_BE_FILLED_IN)])
    repeat_password = named_field(PasswordField)(
        'Повторите пароль', validators=[
            Optional(), EqualTo('password', PASSWORDS_DO_NOT_MATCH)]
    )

    submit = SubmitField('Сохранить изменения')
