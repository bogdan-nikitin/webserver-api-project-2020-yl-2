"""Модуль с различными функциями для взаимодействия с моделью чатов."""

from flask_restful import abort

from app.data import db_session
from app.data.chats import Chats


def get_chat(session, first_user, second_user):
    chat = session.query(Chats).filter(
        ((Chats.first_author_id == first_user.alternative_id) &
         (Chats.second_author_id == second_user.alternative_id)) |
        ((Chats.first_author_id == second_user.alternative_id) &
         (Chats.second_author_id == first_user.alternative_id))).first()
    return chat


def abort_if_chat_not_found(chat_id):
    session = db_session.create_session()
    chat = session.query(Chats).get(chat_id)
    if not chat:
        abort(404, message=f'Chat {chat_id} not found')
