"""Модуль, отвечающий за создание различных частей приложения, которые будут
прикреплены к нему на этапе инициализации"""

import requests
import urllib.parse
from app.api_utils import UserAPIModel, refresh_user
# import jwt
# from flask_login.login_manager import LoginManager
from flask_mail import Mail
from flask_socketio import SocketIO
from flask import redirect, url_for, request, make_response
from modules import constants
# from app.auth_utils import decode_auth_token
# from app.data import db_session
# from app.data.users import Users
from flask_jwt_extended import (
    JWTManager, set_access_cookies,
)
import logging
from flask_wtf.csrf import CSRFProtect, generate_csrf
# login_manager = LoginManager()


mail = Mail()
socketio = SocketIO()
jwt = JWTManager()
csrf = CSRFProtect()


@jwt.unauthorized_loader
def unauthorized_loader(msg):
    return redirect(url_for('main.login'))


@jwt.user_loader_callback_loader
def user_loader(identity):
    return UserAPIModel(identity)


@jwt.expired_token_loader
def expired_token_loader(msg):
    r = make_response(redirect(request.path))
    try:
        refresh_user(r)
        return r
    except Exception as e:
        logging.warning(e)
    return redirect(url_for('main.login'))
