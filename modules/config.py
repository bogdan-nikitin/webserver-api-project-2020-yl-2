"""Модуль, содержащий считанный главный конфиг файл в виде объекта
configparser.RawConfigParser."""

from configparser import RawConfigParser
from modules import constants


config = RawConfigParser()
# По умолчанию все ключи конвертируются в нижний регистр. Следующая строка
# переопределяет метода класса ConfigParser, благодаря чему регистр ключей
# сохраняется
config.optionxform = str
config.read(constants.CONFIG_PATH)
