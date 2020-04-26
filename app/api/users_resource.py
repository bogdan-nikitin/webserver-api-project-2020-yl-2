import flask_login
from flask import jsonify
from flask_restful import Resource, abort

from app.data import db_session
from app.data.users import Users
from app.api.resource_arguments.users_args import post_parser, put_parser


def abort_if_not_found(user_id):
    session = db_session.create_session()
    user = session.query(Users).get(user_id)
    if not user:
        abort(404, message=f'Пользователь {user_id} не найден')


class UsersResource(Resource):
    def get(self, user_id=None):
        if user_id is None:
            user_id = flask_login.current_user.id
        abort_if_not_found(user_id)
        session = db_session.create_session()
        user = session.query(Users).get(user_id)
        if (flask_login.current_user.is_authenticated and
                user.alternative_id == flask_login.current_user.alternative_id):
            return jsonify({'user': user.to_dict(
                only=('alternative_id', 'first_name', 'second_name', 'email',
                      'phone_number', 'age', 'city', 'additional_inf',
                      'is_confirmed', 'api_key', 'avatar', 'created_date')
            )})
        if user in flask_login.current_user.friends:
            return jsonify({'user': user.to_dict(
                only=('alternative_id', 'first_name', 'second_name',
                      'phone_number', 'age', 'city', 'additional_inf',
                      'is_confirmed', 'api_key', 'avatar', 'created_date')
            )})
        return jsonify({'user': user.to_dict(
            only=('first_name', 'second_name')
        )})

    def put(self, user_id):
        abort_if_not_found(user_id)
        args = put_parser.parse_args()
        session = db_session.create_session()
        user = session.query(Users).get(user_id)
        user.first_name = args.get('first_name') or user.first_name
        user.second_name = args.get('second_name') or user.second_name
        user.email = args.get('email') or user.email
        user.phone_number = args.get('phone_number') or user.phone_number
        user.age = args.get('age') or user.age
        user.additional_inf = args.get('additional_inf') or user.additional_inf
        user.city = args.get('city') or user.city
        user.avatar = args.get('avatar') or user.avatar
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def post(self):
        args = post_parser.parse_args()
        session = db_session.create_session()
        if args['password'] != args['password_again']:
            return jsonify({'error': 'Passwords do not match'})
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
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
