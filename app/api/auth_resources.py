import datetime

from flask import jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token, get_jwt_identity,
    jwt_refresh_token_required
)
from flask_restful import Resource, abort

from app.api.resource_arguments.auth_args import login_post_parser
# from app.auth_utils import create_auth_token
from app.data import db_session
from app.data.users import Users


class LoginResource(Resource):
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
    def post():
        args = login_post_parser.parse_args()
        email = args.email
        session = db_session.create_session()
        user: Users = session.query(Users).filter(Users.email == email).first()
        if not user or not user.check_password(args.password):
            abort(404, message='Bad email or password')
            return
        user_id = user.alternative_id
        try:
            if expires_in := args.get('expires_in'):
                expires_in = datetime.timedelta(seconds=expires_in)
        except OverflowError:
            return jsonify({'error': 'expires_in value too big'})
        access_token = create_access_token(identity=user_id,
                                           expires_delta=expires_in)
        refresh_token = create_refresh_token(identity=user_id)
        return jsonify(access_token=access_token, refresh_token=refresh_token)
        # token = create_auth_token({'aud': user.get_id()})
        # return jsonify({'access_token': token})

    # @staticmethod
    # def post():
    #     # TODO Создано для проверки, нужно удалить
    #     from flask_restful.reqparse import RequestParser
    #     parser_ = RequestParser()
    #     parser_.add_argument('email', required=True)
    #     parser_.add_argument('first_name', required=True)
    #     parser_.add_argument('second_name', required=True)
    #     parser_.add_argument('password', required=True)
    #     args = parser_.parse_args()
    #
    #     user = Users()
    #     user.first_name = args.first_name
    #     user.second_name = args.second_name
    #     user.email = args.email
    #     user.set_attributes(args.password)
    #     session = db_session.create_session()
    #     session.add(user)
    #     session.commit()
    #
    #     return jsonify({'user_id': user.alternative_id})


class RefreshResource(Resource):
    @staticmethod
    @jwt_refresh_token_required
    def post():
        user_id = get_jwt_identity()
        if user_id:
            ret = {
                'access_token': create_access_token(identity=user_id)
            }
            return jsonify(ret)
        else:
            return jsonify({'message': 'Error. No refresh token'})

    # @staticmethod
    # @jwt_refresh_token_required
    # def post():
    #     # print(request.json)
    #     print(request.args)
    #     user_id = get_jwt_identity()
    #     # print(user_id)
    #     if user_id:
    #         ret = {
    #             'access_token': create_access_token(identity=user_id),
    #             'refresh_token': create_refresh_token(identity=user_id)
    #         }
    #         return jsonify(ret)
    #     else:
    #         return jsonify({'message': 'Error. No refresh token'})
