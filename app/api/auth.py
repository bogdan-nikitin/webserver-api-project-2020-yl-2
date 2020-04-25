from flask import jsonify, abort
from flask_restful import Resource

from app.api.auth_args import parser
from app.auth_utils import create_auth_token
from app.data import db_session
from app.data.users import Users


class AuthResource(Resource):
    """Ресурс авторизации.
    GET: Возвращает ключ доступа к API в формате {access_key: "ключ"}. Параметры
    запроса:
        email: адрес электронной почти пользователя, для которого нужно получить
        API ключ;
        password: пароль этого пользователя.
    Если такого email нет, возвращается ошибка 404. Если пароль неверный -
    ошибка 401.
    Если все данные верны, возвращается JWT токен, содержащий alternative_id
    пользователя."""

    @staticmethod
    def get():
        args = parser.parse_args()
        email = args.email
        session = db_session.create_session()
        user: Users = session.query(Users).filter(Users.email == email).first()
        if not user:
            abort(404, message=f'User with email {email} not found')
            return
        password = args.password
        if not user.check_password(password):
            abort(401, message='Bad password')
            return
        token = create_auth_token({'aud': user.get_id()})
        return jsonify({'access_token': token})
