"""Модуль, содержащий все конфигруации приложения."""


class Config:
    pass


class DevelopmentConfig:
    SECRET_KEY = 'py_messages_test_secret_key'
    # Для рассылки email, необходимо заполнить следующие поля:
    # MAIL_SERVER =
    # MAIL_PORT =
    # MAIL_USE_TLS =
    # MAIL_USE_SSL =
    # MAIL_USERNAME =
    # MAIL_PASSWORD =
    # MAIL_DEFAULT_SENDER =
    # Бесплатные SMTP сервера можно найти тут:
    # https://bimailer.ru/help/smtp-list.php
    # К примеру, такие услуги предоставляет Google и Яндекс
    # При тестировании приложения эти поля можно не заполнять, тогда сообщение
    # и получатель будут выведены в журнал
