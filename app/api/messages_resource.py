import flask_login
from flask import jsonify
from flask_restful import Resource, abort

from app.data import db_session
from app.data.users import Users
from app.data.messages import Messages
from app.data.chats import Chats
from app.api.resource_arguments.messages_args import post_parser


def abort_if_not_found(obj_id, obj_class):
    session = db_session.create_session()
    obj = session.query(obj_class).get(obj_id)
    if not obj:
        abort(404, message=f'Объекст класса {obj_class}'
                           f' с id {obj_id} не найден')


def abort_if_user_not_found_by_alt_id(alt_id):
    session = db_session.create_session()
    user = session.query(Users).filter(Users.alternative_id == alt_id)
    if not user:
        abort(404, message=f'Пользователь с alternative_id {alt_id} не найден')


class MessagesResource(Resource):
    @flask_login.login_required
    def post(self):
        args = post_parser.parse_args()
        session = db_session.create_session()
        message = Messages(
            sender_id=args['sender_id'],
            chat_id=args['chat_id'],
            text=args['text']
        )
        session.add(message)
        session.commit()
        return jsonify({'success': 'OK'})


class MessagesListResource(Resource):
    @flask_login.login_required
    def get(self, alt_id=None, date=None):
        res = []
        session = db_session.create_session()
        if alt_id and date:
            abort_if_user_not_found_by_alt_id(alt_id)
            user = session.query(Users).filter(Users.alternative_id == alt_id)
            for message in user.messages:
                if message.created_date > date:
                    chat_id = message.chat_id
                    abort_if_not_found(chat_id, Chats)
                    chat = session.query(Chats).get(chat_id)
                    for chat_participant in chat.chat_participants:
                        if chat_participant.user_id ==\
                                flask_login.current_user.id:
                            res.append(message)
            return res
        elif alt_id:
            abort_if_user_not_found_by_alt_id(alt_id)
            user = session.query(Users).filter(Users.alternative_id == alt_id)
            for message in user.messages:
                chat_id = message.chat_id
                abort_if_not_found(chat_id, Chats)
                chat = session.query(Chats).get(chat_id)
                for chat_participant in chat.chat_participants:
                    if chat_participant.user_id == flask_login.current_user.id:
                        res.append(message)
            return res
        else:
            for friend in flask_login.current_user.friends:
                for message in friend.messages[::-1]:
                    message_found = False
                    chat_id = message.chat_id
                    abort_if_not_found(chat_id, Chats)
                    chat = session.query(Chats).get(chat_id)
                    for chat_participant in chat.chat_participants:
                        if chat_participant.user_id ==\
                                flask_login.current_user.id:
                            res.append(message)
                            message_found = True
                    if message_found:
                        break
            return res
