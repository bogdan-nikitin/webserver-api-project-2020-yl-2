"""Главный файл программы, запускает приложение и настраивает журналирование."""

from app import create_app
from modules.config import config
import logging


if __name__ == '__main__':

    # Настройка журналирования
    logging.basicConfig(**config['logging'])

    # Создание и запуск приложения
    app = create_app()
    app.run()


