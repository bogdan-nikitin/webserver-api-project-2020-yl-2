import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Chats(SqlAlchemyBase):
    __tablename__ = 'chats'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    first_author_id = sqlalchemy.Column(sqlalchemy.Integer,
                                        sqlalchemy.ForeignKey('users.id'),
                                        nullable=False)
    second_author_id = sqlalchemy.Column(sqlalchemy.Integer,
                                         sqlalchemy.ForeignKey('users.id'),
                                         nullable=False)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True, default=None)
    chat_participants = orm.relation('ChatParticipants', backref='chats')
