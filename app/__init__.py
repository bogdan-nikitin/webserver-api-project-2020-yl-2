"""Пакет приложения. Содержит фабрику приложений create_app, а также функции,
используемые в обработчике шаблонов Jinja2."""

import logging
import os
import re

from flask import Flask
from flask_restful import Api

from app.api import auth
from app.data import db_session
from app.setup_app import *
from app.socketio_namespaces import socket_index, socket_main
from app.views import main, uploads
from modules import constants


def translate_wtforms_error(error_text):
    """Функция переводит ошибки, генерируемые полями из модуля wtforms на
    русский язык. Если перевода ошибки не найдено, возвращается оригинальный
    текст."""
    translation = constants.WTFORMS_ERRORS_TRANSLATION.get(
        error_text, error_text)
    return translation


def create_app() -> Flask:
    """Фабрика приложений. Создаёт приложение. Конфигурация происходит следующим
    образом:
    Получается значение переменной среды (далее - переменной) APP_CONFIG.
    Если значение этой переменной является путём к файлу, то вызывается функция
    app.config.from_envvar() с переданным значением переменной APP_CONFIG. Иначе
    значение переменной расценивается как название Python класса и вызывается
    функция app.config.from_object() с переданным значением этой переменной.

    Все конфиги должны содержаться в файле app/config.py.

    По умолчанию APP_CONFIG = app.config.DevelopmentConfig.

    Чтобы сконфигурировать приложение через переменные среды, установите
    значение APP_CONFIG = app.config.EnvConfig, в переменную APP_ENV_VARS
    внесите через запятую названия всех значений конфигурации, которые вы хотите
    установить через переменные среды, и соотвествующим переменным среды
    присвойте нужные значения (учитите, что эти значения вычисляются как Python
    выражения с помощью функции eval()). Подробнее в app.config.EnvConfig.

    :return: Flask-приложение
    :rtype: Flask
    """
    app = Flask(__name__)

    # Конфигурация приложения
    app_config = os.environ.get('APP_CONFIG', 'app.config.DevelopmentConfig')
    logging.info('Конфигурация через %s', app_config)
    if os.path.isfile(app_config):
        app.config.from_pyfile(app_config)
    else:
        app.config.from_object(app_config)

    # Инициализация частей приложения
    login_manager.init_app(app)
    mail.app = app
    mail.init_app(app)
    socketio.init_app(app)
    api_ = Api(app)

    # Настройка частей приложения
    login_manager.login_view = 'main.login'

    # Регистрация пространств имён Socket.IO
    socketio.on_namespace(socket_index.IndexNamespace('/index'))
    socketio.on_namespace(socket_main.MainNamespace('/'))

    # Регистрация чертежей
    app.register_blueprint(main.blueprint)
    app.register_blueprint(uploads.blueprint)

    # Регистрация API
    api_.add_resource(auth.AuthResource, '/api/v1/auth')

    # Настройки окружения Jinja2
    app.jinja_env.add_extension('jinja2.ext.do')
    app.jinja_env.globals['print'] = print
    app.jinja_env.globals['bool'] = bool
    app.jinja_env.globals[
        'translate_wtforms_error'] = translate_wtforms_error
    app.jinja_env.globals['re'] = re
    app.jinja_env.globals['constants'] = constants

    # Инициализация БД
    db_session.global_init(constants.DB_PATH)
    return app
