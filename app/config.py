"""Модуль, содержащий все конфигруации приложения."""
import os

from modules import constants


class Config:
    pass


class DevelopmentConfig(Config):
    SECRET_KEY = 'py_messages_test_secret_key'
    UPLOAD_FOLDER = constants.UPLOAD_PATH
    ENV = 'development'
    DEBUG = True
    # Для рассылки email, необходимо заполнить следующие поля:
    # MAIL_SERVER =
    # MAIL_PORT =
    # MAIL_USE_TLS =
    # MAIL_USE_SSL =
    # MAIL_USERNAME =
    # MAIL_PASSWORD =
    # MAIL_DEFAULT_SENDER =
    # При тестировании приложения эти поля можно не заполнять, тогда сообщение
    # и получатель будут выведены в журнал


# Во время конфигурации Flask не создаёт экземпляры классов конфигураций, а
# использует сами классы. Чтобы динамически присвоить полям класса значения
# динамически (фактически создать объект класса на лету), приходится
# использовать метаклассы

# Коротко о метаклассах:
# Объект - экземпляр класса
# Класс - экзепляр метакласса

class _EnvConfigMetaclass(type):
    """Метакласс класса EnvConfig. Создаёт все необходимые поля по описанному в
    классе EnvConfig способу."""

    def __new__(mcs, cls_name, bases, cls_attrs):

        if flask_vars := os.environ.get('APP_ENV_VARS'):
            flask_vars_list = flask_vars.split(',')
            for flask_var in flask_vars_list:
                flask_var = flask_var.strip()
                if value := os.environ.get(flask_var):
                    cls_attrs[flask_var] = eval(value)
        return super(_EnvConfigMetaclass, mcs).__new__(mcs,
                                                       cls_name,
                                                       bases,
                                                       cls_attrs)


class EnvConfig(Config, metaclass=_EnvConfigMetaclass):
    """Конфигурация из переменных среды. В переменной среды APP_ENV_VARS через
    запятую перечисляются переменные среды, которые будут использованы для
    конфигурации приложения. Во время создания класса (в метаклассе
    _EnvConfigMetaclass) значение каждой перечисленной переменной
    выполняется как выражение Python с помощью функции eval(), а затем
    полученные значения присваиваются соотвествующим полям этого класса.

    :Example:

    В консоли / терминале
    set APP_CONFIG = app.config.EnvConfig
    set APP_ENV_VARS = SECRET_KEY, DEBUG
    set SECRET_KEY = 'SUPER_SECRET_KEY'
    set DEBUG = True
    В коде приложения
    >>> EnvConfig.SECRET_KEY
    'SUPER_SECRET_KEY'
    >>> EnvConfig.DEBUG
    True
    """
