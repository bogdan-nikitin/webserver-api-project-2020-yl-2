import flask_login
from flask import jsonify
from flask_restful import Resource, abort

from app.data import db_session
from app.data.users import Users
from app.data.chats import Chats
from app.data.messages import Messages
# from app.data.chat_participants import ChatParticipants
from app.api.resource_arguments.chats_args import post_parser, delete_parser


def abort_if_not_found(chat_id):
    session = db_session.create_session()
    chat = session.query(Chats).get(chat_id)
    if not chat:
        abort(404, message=f'Чат {chat_id} не найден')


def abort_if_user_not_found_by_alt_id(alt_id):
    session = db_session.create_session()
    user = session.query(Users).filter(Users.alternative_id == alt_id)
    if not user:
        abort(404, message=f'Пользователь с alternative_id {alt_id} не найден')


class ChatsResource(Resource):
    @flask_login.login_required
    def get(self):
        return flask_login.current_user.chats

    @flask_login.login_required
    def post(self):
        # метод post с помощью ChatParticipants

        # args = post_parser.parse_args()
        # chat_participants = args['chat_participants']
        # chat = Chats(
        #     title=args.get('title')
        # )
        # session = db_session.create_session()
        # session.add(chat)
        # for user in chat_participants:
        #     chat_participants_obj = ChatParticipants(
        #         user_id=user.id,
        #         chat_id=chat.id
        #     )
        #     session.add(chat_participants_obj)
        # session.commit()
        # return jsonify({'success': 'OK'})

        args = post_parser.parse_args()
        chat = Chats(
            title=args.get('title'),
            first_author_id=args['first_author_id'],
            second_author_id=args['second_author_id']
        )
        session = db_session.create_session()
        session.add(chat)
        session.commit()
        return jsonify({'success': 'OK'})

    @flask_login.login_required
    def delete(self):
        args = delete_parser.parse_args()
        alt_id = args.get('alternative_id')
        chat_id = args.get('id')
        if chat_id:
            abort_if_not_found(chat_id)
            session = db_session.create_session()
            chat = session.query(Chats).get(chat_id)
            messages = session.query(Messages).filter(
                Messages.chat_id == chat_id)
            for message in messages:
                session.delete(message)
            session.delete(chat)
            session.commit()
        elif alt_id:
            abort_if_user_not_found_by_alt_id(alt_id)
            session = db_session.create_session()
            user_id = session.query(Users).filter(
                Users.alternative_id == alt_id).id
            cur_user_id = flask_login.current_user.id
            chat = session.query(Chats).filter(
                ((Chats.first_author_id == user_id)
                 | (Chats.first_author_id == cur_user_id))
                and ((Chats.second_author_id == user_id)
                     | (Chats.second_author_id == cur_user_id)))
            session.delete(chat)
            session.commit()
        return jsonify({'success': 'OK'})
