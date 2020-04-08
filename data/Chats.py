import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Chats(SqlAlchemyBase):
    __tablename__ = 'chats'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True, default=None)
    chat_participants = orm.relation('ChatParticipants', backref='chat')
