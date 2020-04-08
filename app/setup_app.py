"""Модуль, отвечающий за создание различных частей приложения, которые будут
прикреплены к нему на этапе инициализации"""

from flask_login.login_manager import LoginManager


login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return  # TODO Заглушка. Нужно переделать
