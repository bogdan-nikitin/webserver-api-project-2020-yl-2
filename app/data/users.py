import random
import string
import datetime
import hashlib

import sqlalchemy
from flask import current_app
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.data import db_session

from .db_session import SqlAlchemyBase
from .users_friends import UsersFriends


def create_alternative_id(size):
    alt_ids = set()
    session = db_session.create_session()
    for user in session.query(Users).all:
        alt_ids.add(user.alternative_id)
    alt_id = ''.join(
        random.choice(string.ascii_letters + string.digits + '_' * 13) for _ in
        range(size))
    while alt_id in alt_ids:
        alt_id = ''.join(
            random.choice(string.ascii_letters + string.digits + '_' * 13)
            for _ in range(size))
    return alt_id


def create_api_key(email, created_date, password):
    secret_key = current_app.config['SECRET_KEY']
    hash_object = hashlib.sha256(bytes(email + secret_key + str(created_date) +
                                       password, encoding='utf-8'))
    return hash_object.hexdigest()


class Users(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    alternative_id = sqlalchemy.Column(sqlalchemy.String)
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
    api_key = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    avatar = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

    messages = orm.relation('Messages', backref='message_sender')
    chats = orm.relation('Chats', secondary='chat_participants',
                         backref='chat_member')
    friends = orm.relation('UsersFriends', backref='inviter',
                           foreign_keys=[UsersFriends.inviter_id])

    def set_attributes(self, password):
        self.hashed_password = generate_password_hash(password)
        self.api_key = create_api_key(self.email, self.created_date, password)
        self.alternative_id = create_alternative_id(random.randint(10, 20))

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
