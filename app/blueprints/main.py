"""Модуль содержит основные обработчики тех страниц, которые будут видеть
обычные пользователи."""

import logging
import urllib.parse

from flask import (Blueprint, render_template, redirect, url_for, abort,
                   session)
from flask_login import current_user
from flask_mail import Message

from app.email import send_msg_in_thread
from app.forms import LoginForm, RegisterForm
from app.verify_email import create_token
from modules import constants

blueprint = Blueprint('main', __name__)


@blueprint.route('/', methods=['POST', 'GET'])
def index():
    # TODO Заглушка. Может только отображать форму входа.
    if not current_user.is_authenticated:
        return login()
    return 'TODO'


@blueprint.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # TODO Добавить аутентификацию пользователя
        return redirect(url_for('main.index'))
    param = {
        'title': 'Войти в PyMessages',
        'form': form
    }
    return render_template('login.jinja2', **param)


@blueprint.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # TODO Добавить внесение данных пользователя в БД
        email = form.email.data

        # Сохраняем email в сессии, чтобы дать пользователю ссылку на его
        # почтовый ящик на странице подтверждения email
        session['email'] = email

        # Создаём токен, по которому будем подтверждать email пользователя и
        # отправляем ему ссылку с подтверждением на email
        # TODO Добавить внесение токена в БД, вставить реальную дату
        token = create_token(email, 'account_create_date')
        msg = Message('Подтвердите свой email - PyMessages', recipients=[email])
        mail_param = {
            'verify_url': url_for('main.verify_email', token=token,
                                  _external=True)
        }
        msg.html = render_template('verify_email_msg.jinja2', **mail_param)
        # Если не удалось отправить сообщение, то выводим сообщение об ошибке,
        # получателя и текст письма
        try:
            send_msg_in_thread(msg)
        except Exception as e:
            log_msg = ('Возникло исключение при отправке письма: \n%s\n'
                       'Вероятнее всего, вы забыли настроить конфиг '
                       'приложения.\nЧтобы настроить конфиг, перейдите в '
                       'файл app/config.py и заполните все необходимые поля.')
            logging.warning(log_msg, e)
            logging.debug(email + '\n' + msg.html)
        # Отправляем пользователя на страницу с просьбой проверить почту
        return redirect(url_for('main.verify_email', token=''))
    param = {
        'title': 'Регистрация в PyMessages',
        'form': form
    }
    return render_template('register.jinja2', **param)


@blueprint.route('/verify_email/')
def verify_email_message():
    # Если пользователь только что создал аккаунт и указал рабочую почту, то
    # просим его перейти в почтовый ящик и подтвердить почту
    email = session.get('email')
    if email and '@' in email:
        mail_domain = email[email.index('@') + 1:]
        # Ищем URL почты пользователя,
        email_server = constants.MAIL_DOMAINS_URLS.get(mail_domain)
        # если не находим, даём ссылку на домен почты
        if email_server:
            email_server = urllib.parse.urlunsplit(
                ('http', mail_domain, *[''] * 3)
            )
    else:
        abort(403)
        return
    param = {
        'title': 'Подтвердите email - PyMessages',
        'email_server': email_server
    }
    return render_template('verify_email.jinja2', **param)


@blueprint.route('/verify_email/<string:token>')
def verify_email(token):
    if token == token:  # TODO Добавить получение и проверку токена из БД
        # TODO Добавить подтверждение пользователя
        param = {
            'title': 'Email подтверждён - PyMessages'
        }
        return render_template('email_verified.jinja2', **param)
    abort(403)
