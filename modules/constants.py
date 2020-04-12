"""Модуль содержит большинство констант."""
import os

# Выделил родительскую директорию в отдельную переменную, дабы при перемещении
# этого файла в PyCharm путь автоматически менялся (если сразу передать путь в
# функцию ниже, то PyCharm его не распознает как путь)
__parent_dir = '..'
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        __parent_dir))
LOGGING_CONFIG_FILE = os.path.join(ROOT_DIR, 'logging.ini')

APP_CONFIG = 'app.config.DevelopmentConfig'

# Перевод ошибок wtforms
WTFORMS_ERRORS_TRANSLATION = {
    'This field is required.': 'Это поле необходимо заполнить',
    'Invalid email address.': 'Неверный адрес электронной почты'
}
WTFORMS_FIELD_MUST_BE_EQUAL_ERROR = r'Field must be equal to (.+)\.'

PAGE_NAV_LINKS = {
    'Главная': 'main.index',
    'Вход': 'main.login',
    'Регистарция': 'main.register'
}

MAIL_DOMAINS_URLS = {
    "mail.ru": "https://e.mail.ru/",
    "bk.ru": "https://e.mail.ru/",
    "list.ru": "https://e.mail.ru/",
    "inbox.ru": "https://e.mail.ru/",
    "yandex.ru": "https://mail.yandex.ru/",
    "ya.ru": "https://mail.yandex.ru/",
    "yandex.ua": "https://mail.yandex.ua/",
    "yandex.by": "https://mail.yandex.by/",
    "yandex.kz": "https://mail.yandex.kz/",
    "yandex.com": "https://mail.yandex.com/",
    "gmail.com": "https://mail.google.com/",
    "googlemail.com": "https://mail.google.com/",
    "outlook.com": "https://mail.live.com/",
    "hotmail.com": "https://mail.live.com/",
    "live.ru": "https://mail.live.com/",
    "live.com": "https://mail.live.com/",
    "me.com": "https://www.icloud.com/",
    "icloud.com": "https://www.icloud.com/",
    "rambler.ru": "https://mail.rambler.ru/",
    "yahoo.com": "https://mail.yahoo.com/",
    "ukr.net": "https://mail.ukr.net/",
    "i.ua": "http://mail.i.ua/",
    "bigmir.net": "http://mail.bigmir.net/",
    "tut.by": "https://mail.tut.by/",
    "inbox.lv": "https://www.inbox.lv/",
    "mail.kz": "http://mail.kz/"
}

ADDITIVE_TYPES_TITLES = ['photo', 'video', 'audio', 'sticker', 'file']

DB_PATH = os.path.join(ROOT_DIR, 'db/messenger.sqlite3')
