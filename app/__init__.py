"""Пакет приложения. Содержит фабрику приложений create_app, а также функции,
используемые в обработчике шаблонов Jinja2."""

from app.setup_app import *
from flask import Flask
from app.blueprints import main
from modules import constants
from modules.config import config


def translate_wtforms_error(error_text):
    """Функция переводит ошибки, генерируемые полями из модуля wtforms на
    русский язык. Если перевода ошибки не найдено, возвращается оригинальный
    текст."""
    return constants.WTFORMS_ERRORS_TRANSLATION.get(error_text, error_text)


def setup_from_config(app):
    """Загрузка всех настроек приложения из конфиг файла."""
    for option, value in config.items('app.config'):
        app.config[option] = value


def create_app() -> Flask:
    """Фабрика приложений. Создаёт приложение

    :return: Flask-приложение
    :rtype: Flask
    """
    app = Flask(__name__)

    # Инициализация частей приложения
    login_manager.init_app(app)

    # Регистрация чертежей
    app.register_blueprint(main.blueprint)

    # Конфигурация приложения
    setup_from_config(app)

    # Настройки окружения Jinja2
    app.jinja_env.globals[
        'translate_wtforms_error'] = translate_wtforms_error
    app.jinja_env.add_extension('jinja2.ext.do')
    app.jinja_env.globals['print'] = print

    return app
