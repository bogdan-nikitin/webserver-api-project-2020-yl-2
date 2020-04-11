"""Модуль, отвечающий за создание различных частей приложения, которые будут
прикреплены к нему на этапе инициализации"""

from flask_login.login_manager import LoginManager
from flask_mail import Mail


login_manager = LoginManager()
mail = Mail()


@login_manager.user_loader
def load_user(user_id):
    return  # TODO Заглушка. Нужно переделать
