import datetime
import random
import string
from modules.anything import anything

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.data import db_session
from app.data.db_session import SqlAlchemyBase
from app.data.users_friends import UsersFriends
from functools import wraps


def generate_alternative_id():
    size = random.randint(10, 20)
    alt_id = ''.join(
        random.choice(string.ascii_letters + string.digits + '_') for _ in
        range(size)).lower()
    return alt_id


def create_alternative_id():
    session = db_session.create_session()
    alt_id = generate_alternative_id()
    query = session.query(Users).exists().where(
        Users.alternative_id == 123)
    while session.query(query).scalar():
        alt_id = generate_alternative_id()
    return alt_id


class Users(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True,
                           index=True)
    alternative_id = sqlalchemy.Column(sqlalchemy.String, index=True)
    first_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    second_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=False)
    phone_number = sqlalchemy.Column(sqlalchemy.Integer, unique=True,
                                     nullable=True)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    city = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    additional_inf = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    is_confirmed = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    avatar = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    messages = orm.relation('Messages', backref='message_sender')
    chats = orm.relation('Chats', secondary='chat_participants',
                         backref='chat_member')
    incoming_friend_requests = orm.relation(
        'UsersFriends', backref='inviter',
        foreign_keys=[UsersFriends.invitee_id]
    )
    outgoing_friend_requests = orm.relation(
        'UsersFriends', backref='invitee',
        foreign_keys=[UsersFriends.inviter_id]
    )

    @property
    def friends(self):
        session = db_session.create_session()
        friends_list = FriendsList()
        users_query = session.query(Users)
        for friend in self.incoming_friend_requests:
            if friend.is_accepted:
                user = users_query.filter(Users.id == friend.inviter_id).first()
                friends_list.append(user)
        for friend in self.outgoing_friend_requests:
            if friend.is_accepted:
                user = users_query.filter(Users.id == friend.invitee_id).first()
                friends_list.append(user)
        return friends_list

    def set_attributes(self, password):
        self.hashed_password = generate_password_hash(password)
        self.alternative_id = create_alternative_id()

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    @wraps(SerializerMixin.to_dict)
    def to_dict(self, *args, **kwargs):
        result = super().to_dict(*args, **kwargs)
        if 'alternative_id' in result:
            result['user_id'] = result['alternative_id']
            del result['alternative_id']
        return result


class FriendsList(list):
    def __contains__(self, user: Users):
        return any(friend.id == user.id for friend in self)