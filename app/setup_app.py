"""Модуль, отвечающий за создание различных частей приложения, которые будут
прикреплены к нему на этапе инициализации"""

import functools

from flask_login import current_user
from flask_login.login_manager import LoginManager
from flask_mail import Mail
from flask_socketio import SocketIO
from flask_socketio import disconnect

login_manager = LoginManager()
mail = Mail()
socketio = SocketIO()


@login_manager.user_loader
def load_user(user_id):
    # TODO Заглушка. Переделать
    return


def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)

    return wrapped

# @login_manager.request_loader
# def load_user_from_request(request):
#     print('request_loader called')
#     auth_headers = request.headers.get('Authorization', '').split()
#     if len(auth_headers) == 2 and auth_headers[0] == 'Bearer':
#         token = auth_headers[1]
#     elif request.json and 'access_token' in request.json:
#         token = request.json['access_token']
#     else:
#         return
#     try:
#         data = jwt.decode(token, current_app.config['SECRET_KEY'])
#     except jwt.ExpiredSignatureError:
#         return
#     except (jwt.InvalidTokenError, Exception) as e:
#         return
