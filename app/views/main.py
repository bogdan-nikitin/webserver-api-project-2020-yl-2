"""Модуль содержит основные обработчики тех страниц, которые будут видеть
обычные пользователи."""

import logging
import urllib.parse

import flask
from flask import Blueprint, render_template, redirect, url_for, abort
from flask_login import current_user, login_required, logout_user
from flask_mail import Message

from app.auth_utils import create_email_token
from app.email_utils import send_msg_in_thread
from app.forms import *
from modules import constants

blueprint = Blueprint('main', __name__)


@blueprint.route('/index', methods=['POST', 'GET'])
@blueprint.route('/', methods=['POST', 'GET'])
def index():
    # TODO Добавить login_required, убрать проверку ниже
    if not current_user.is_authenticated and False:
        return login()
    param = {
        'title': 'PyMessages'
    }
    return render_template('index.jinja2', **param)


@blueprint.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # TODO Добавить аутентификацию пользователя
        return redirect(url_for('main.index'))
    param = {
        'title': 'Войти в PyMessages',
        'form': form,
        'error_msg': None  # Тут можно указать ошибку при валидации формы
    }
    return render_template('login.jinja2', **param)


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@blueprint.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    form = RegisterForm()
    if form.validate_on_submit():
        # TODO Добавить внесение данных пользователя в БД
        email = form.email.data

        # Сохраняем email в сессии, чтобы дать пользователю ссылку на его
        # почтовый ящик на странице подтверждения email
        flask.session['email'] = email

        # Создаём токен, по которому будем подтверждать email пользователя и
        # отправляем ему ссылку с подтверждением на email
        # TODO Добавить внесение токена в БД, вставить реальную дату
        token = create_email_token(email, 'account_create_date')
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
        'form': form,
        'error_msg': None  # Тут можно указать ошибку при валидации формы
    }
    return render_template('register.jinja2', **param)


@blueprint.route('/verify_email/')
def verify_email_message():
    if current_user.is_authenticated:
        return redirect('/')
    # Если пользователь только что создал аккаунт и указал рабочую почту, то
    # просим его перейти в почтовый ящик и подтвердить почту
    email = flask.session.get('email')
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
        'email_server': email_server,
    }
    return render_template('verify_email.jinja2', **param)


@blueprint.route('/verify_email/<string:token>')
def verify_email(token):
    if current_user.is_authenticated:
        return redirect('/')
    if token == token:  # TODO Добавить получение и проверку токена из БД
        # TODO Добавить подтверждение пользователя
        param = {
            'title': 'Email подтверждён - PyMessages',
        }
        return render_template('email_verified.jinja2', **param)
    abort(403)


@blueprint.route('/profile', methods=['GET', 'POST'])
# TODO Добавить login_required
def profile():
    info_form = ChangeProfileInfoForm(prefix='info')
    security_form = ChangeProfileSecurityForm(prefix='security')
    # TODO Установить форме по умолчанию текущие данные пользователя
    #  (не считая пароля)
    if info_form.validate_on_submit():
        # TODO Добавить занесение в БД данных из формы, если они указаны
        param = {
            'title': 'Профиль - PyMessages',
            'info_form': info_form,
            'security_form': security_form,
            'info_error_msg': None,
            'info_success_msg': 'Данные успешно изменены',
            'jump_to': 'infoCard'
        }
        return render_template('profile.jinja2', **param)
    elif security_form.validate_on_submit():
        # TODO Добавить занесение в БД данных из формы, если они указаны
        param = {
            'title': 'Профиль - PyMessages',
            'info_form': info_form,
            'security_form': security_form,
            'security_error_msg': None,
            'security_success_msg': 'Данные успешно изменены',
            'jump_to': 'securityCard'
        }
        return render_template('profile.jinja2', **param)

    param = {
        'title': 'Профиль - PyMessages',
        'info_form': info_form,
        'security_form': security_form
    }
    return render_template('profile.jinja2', **param)
