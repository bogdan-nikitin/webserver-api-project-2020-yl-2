"""Модуль, отвечающий за создание различных частей приложения, которые будут
прикреплены к нему на этапе инициализации"""


from flask_login.login_manager import LoginManager
from flask_mail import Mail
from flask_socketio import SocketIO

login_manager = LoginManager()
mail = Mail()
socketio = SocketIO()


@login_manager.user_loader
def load_user(user_id):
    # TODO Заглушка. Переделать
    return

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
