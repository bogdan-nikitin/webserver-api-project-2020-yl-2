"""Модуль содержит большинство констант."""
from configparser import RawConfigParser

CONFIG_PATH = 'config.ini'

config = RawConfigParser()
# По умолчанию все ключи конвертируются в нижний регистр. Следующая строка
# переопределяет метода класса ConfigParser, благодаря чему регистр ключей
# сохраняется
config.optionxform = str
config.read(CONFIG_PATH)

# Перевод ошибок wtforms
WTFORMS_ERRORS_TRANSLATION = {
    'This field is required.': 'Это поле необходимо заполнить',
    'Invalid email address.': 'Неверный адрес электронной почты'
}
