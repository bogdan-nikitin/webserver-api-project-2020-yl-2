"""Пакет приложения. Содержит фабрику приложений create_app, а также функции,
используемые в обработчике шаблонов Jinja2."""

import logging
import re

from flask import Flask
from flask_restful import Api

from app.blueprints import main
from app.setup_app import *
from modules import constants

from app.data import db_session
from app.api import users_resource


def translate_wtforms_error(error_text):
    """Функция переводит ошибки, генерируемые полями из модуля wtforms на
    русский язык. Если перевода ошибки не найдено, возвращается оригинальный
    текст."""
    translation = constants.WTFORMS_ERRORS_TRANSLATION.get(
        error_text, error_text)
    if translation is None:
        logging.warning(f'No translation for wtforms error: {error_text}.')
    return translation


def create_app() -> Flask:
    """Фабрика приложений. Создаёт приложение

    :return: Flask-приложение
    :rtype: Flask
    """
    app = Flask(__name__)

    api = Api(app)
    api.add_resource(users_resource.UsersResource, '/api/users',
                     '/api/users/<int:user_id>')

    # Конфигурация приложения
    app.config.from_object(constants.APP_CONFIG)

    # Инициализация частей приложения
    login_manager.init_app(app)
    mail.app = app
    mail.init_app(app)

    # Регистрация чертежей
    app.register_blueprint(main.blueprint)

    # Настройки окружения Jinja2
    app.jinja_env.add_extension('jinja2.ext.do')
    app.jinja_env.globals['print'] = print
    app.jinja_env.globals[
        'translate_wtforms_error'] = translate_wtforms_error
    app.jinja_env.globals['re'] = re
    app.jinja_env.globals['constants'] = constants

    # Инициализация БД
    db_session.global_init(constants.DB_PATH)

    return app
