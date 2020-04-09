import sqlalchemy
from .db_session import SqlAlchemyBase


class ChatParticipants(SqlAlchemyBase):
    __tablename__ = 'chat participants'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('users.id'))
    chat_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('chats.id'))
