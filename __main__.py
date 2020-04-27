"""Главный файл программы, запускает приложение и настраивает журналирование."""

from app import create_app
import logging.config
from modules.constants import LOGGING_CONFIG_FILE


if __name__ == '__main__':

    # Настройка журналирования
    logging.config.fileConfig(LOGGING_CONFIG_FILE)

    logging.info('Запуск приложения')

    # Создание и запуск приложения
    app = create_app()
    app.run()
