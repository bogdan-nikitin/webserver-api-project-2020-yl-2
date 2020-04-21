from flask import jsonify
from flask_restful import Resource, abort

from app.data import db_session
from app.data.users import Users
from app.api.users_args import parser, parser_edit


def abort_if_not_found(user_id):
    session = db_session.create_session()
    user = session.query(Users).get(user_id)
    if not user:
        abort(404, message=f'Пользователь {user_id} не найден')


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_not_found(user_id)
        session = db_session.create_session()
        user = session.query(Users).get(user_id)
        return jsonify({'user': user.to_dict()})

    def put(self, user_id):
        abort_if_not_found(user_id)
        args = parser_edit.parse_args()
        session = db_session.create_session()
        user = session.query(Users).get(user_id)
        if not args['password']:
            return jsonify({'error': 'Bad request'})
        # для редактирования пользователя нужно знать его пароль
        if not user.check_password(args['password']):
            return jsonify({'error': 'Passwords do not match'})
        user.first_name = args.get('first_name') if args.get('first_name') \
            else user.first_name
        user.second_name = args.get('second_name') if args.get('second_name') \
            else user.second_name
        user.email = args.get('email') if args.get('email') else user.email
        user.phone_number = args.get('phone_number') \
            if args.get('phone_number') else user.phone_number
        user.age = args.get('age') if args.get('age') else user.age
        user.additional_inf = args.get('additional_inf') \
            if args.get('additional_inf') else user.additional_inf
        user.city = args.get('city') if args.get('city') else user.city
        user.avatar = args.get('avatar') if args.get('avatar') else user.avatar
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def post(self):
        args = parser.parse_args()
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
