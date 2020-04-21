import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Messages(SqlAlchemyBase):
    __tablename__ = 'messages'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    sender_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey('users.id'),
                                  nullable=False)
    chat_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('chats.id'),
                                nullable=False)
    text = sqlalchemy.Column(sqlalchemy.String)
    additives = orm.relation('Additives', backref='message')
