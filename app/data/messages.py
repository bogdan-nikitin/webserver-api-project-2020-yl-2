import sqlalchemy
from datetime import datetime
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
    is_read = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    sending_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)
    additives = orm.relation('Additives', backref='message')
