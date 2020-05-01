from flask import jsonify
from flask_jwt_extended import (
    get_jwt_identity, jwt_optional, current_user, jwt_required,
    verify_jwt_in_request, set_access_cookies, set_refresh_cookies
)
from flask_restful import Resource, abort
from app.api.resource_arguments.users_args import *
from app.data import db_session
from app.data.users import Users
from app.data.tokens import Tokens
from app.auth_utils import create_email_token


USERS_PRIVATE_ONLY = (
    'alternative_id', 'first_name', 'second_name', 'email',
    'phone_number', 'age', 'city', 'additional_inf',
    'is_confirmed', 'avatar', 'created_date')
USERS_PUBLIC_ONLY = ('first_name', 'second_name', 'alternative_id')


def abort_if_not_found(user_id):
    session = db_session.create_session()
    user = session.query(Users).filter(Users.alternative_id == user_id).first()
    if not user:
        abort(404, message=f'User {user_id} not found')


def create_token(user, session=None):
    session = session or db_session.create_session()
    token = Tokens(token=create_email_token(user.email),
                   email=user.email)
    session.add(token)
    session.commit()


def users_like(field, val):
    return getattr(Users, field).like('%' + val + '%')


class UsersResource(Resource):
    @staticmethod
    @jwt_optional
    def get(user_id=None):
        user_id = user_id or get_jwt_identity()
        if not user_id:
            abort(400, message='User not specified')
        abort_if_not_found(user_id)
        session = db_session.create_session()
        query = session.query(Users)
        user = query.filter(Users.alternative_id == user_id).first()
        if current_user and user_id == current_user.user_id:
            return jsonify({'user': user.to_dict(only=USERS_PRIVATE_ONLY)})
        # TODO Переделать код ниже
        # if user in flask_login.current_user.friends:
        #     return jsonify({'user': user.to_dict(
        #         only=('alternative_id', 'first_name', 'second_name',
        #               'phone_number', 'age', 'city', 'additional_inf',
        #               'is_confirmed', 'api_key', 'avatar', 'created_date')
        #     )})
        return jsonify({'user': user.to_dict(only=USERS_PUBLIC_ONLY)})

    @staticmethod
    @jwt_required
    def put():
        args = put_parser.parse_args()

        user_id = get_jwt_identity()
        session = db_session.create_session()
        query = session.query(Users)
        user: Users = query.filter(Users.alternative_id == user_id).first()

        old_password = args.old_password
        email = args.email
        password = args.password

        if email or password:
            if not old_password:
                return jsonify(
                    {'error': 'To change email or password you must specify '
                              'your old password'}
                )
            elif not user.check_password(old_password):
                return jsonify({'error': 'Bad password'})

            if email:
                user.email = email
                create_token(user, session=session)
            if password:
                user.set_attributes(password)

        user.first_name = args.get('first_name') or user.first_name
        user.second_name = args.get('second_name') or user.second_name
        user.phone_number = args.get('phone_number') or user.phone_number
        user.age = args.get('age') or user.age
        user.additional_inf = args.get('additional_inf') or user.additional_inf
        user.city = args.get('city') or user.city
        user.avatar = args.get('avatar') or user.avatar
        session.commit()
        return jsonify({'user_id': user.alternative_id})

    @staticmethod
    def post():
        args = post_parser.parse_args()
        session = db_session.create_session()
        if session.query(Users).filter(
                Users.email == args['email']).first():
            return jsonify({'error': 'This user already exists'})
        user = Users(
            first_name=args['first_name'],
            second_name=args['second_name'],
            email=args['email'],
            phone_number=args.get('phone_number'),
            age=args.get('age'),
            additional_inf=args.get('additional_inf'),
            city=args.get('city'),
            avatar=args.get('avatar')
        )
        user.set_attributes(args['password'])
        session.add(user)
        create_token(user, session=session)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    @staticmethod
    def get():
        args = list_get_parser.parse_args()
        if limit := args.get('limit'):
            if limit > constants.USERS_LIST_RESOURCE_GET_COUNT:
                return jsonify({
                    'error': 'Maximum limit is {0}'
                    .format(constants.USERS_LIST_RESOURCE_GET_COUNT)
                })
        else:
            limit = constants.USERS_LIST_RESOURCE_GET_COUNT
        fields = ['first_name', 'second_name', 'alternative_id']
        session = db_session.create_session()
        query = session.query(Users)
        if search_request := args.search_request:
            for word in search_request.split(' '):
                req = users_like(fields[0], word)
                for i in range(0, len(fields) - 1):
                    req = req | users_like(fields[i + 1], word)
                query = query.filter(req)
        else:
            field_names = {'user_id': 'alternative_id'}
            for key in ['first_name', 'second_name', 'user_id']:
                if val := args.get(key):
                    field = field_names.get(key, key)
                    query = query.filter(users_like(field, val))
        start = args.start
        users = query.all()[start:start + limit]
        return jsonify({
            'users': [user.to_dict(only=USERS_PUBLIC_ONLY) for user in users]
        })

