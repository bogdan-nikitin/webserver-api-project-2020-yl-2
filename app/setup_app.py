"""Модуль, отвечающий за создание различных частей приложения, которые будут
прикреплены к нему на этапе инициализации"""

import jwt
from flask_login.login_manager import LoginManager
from flask_mail import Mail
from flask_socketio import SocketIO

from app.auth_utils import decode_auth_token
from app.data import db_session
from app.data.users import Users

login_manager = LoginManager()
mail = Mail()
socketio = SocketIO()


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(Users).filter(Users.alternative_id == user_id).first()


@login_manager.request_loader
def load_user_from_request(request):
    """Загрузка пользователя через запрос"""
    auth_headers = request.headers.get('Authorization', '').split()
    if len(auth_headers) == 2 and auth_headers[0] == 'Bearer':
        token = auth_headers[1]
    elif request.json and 'access_token' in request.json:
        token = request.json['access_token']
    else:
        # abort(
        #     401,
        #     'The access token not specified. Specify the token in the '
        #     '"Authorization" header with the Bearer type, or pass it in the '
        #     '"access_key" request parameter'
        # )
        return
    try:
        data = decode_auth_token(token)
    except jwt.exceptions.InvalidTokenError:
        return
    user_id = data['aud']
    session = db_session.create_session()
    return session.query(Users).filter(Users.alternative_id == user_id).first()
