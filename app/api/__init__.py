"""Модуль, инициализирующий все ресурсы API"""
from flask_restful import Api
from flask import Blueprint
from app.api import (
    users_resource, users_friends_resource, chats_resource, messages_resource,
    tokens_resource, ee, auth_resources
)
api_blueprint = Blueprint('API', __name__)
api_ = Api(api_blueprint)
api_.add_resource(auth_resources.LoginResource, 'login/')
api_.add_resource(auth_resources.RefreshResource, 'refresh/')
api_.add_resource(users_resource.UsersListResource, 'users')
api_.add_resource(users_resource.UsersResource, 'users/',
                  'users/<string:user_id>')
api_.add_resource(users_friends_resource.UsersFriendsListResource,
                  'users_friends')
api_.add_resource(users_friends_resource.UsersFriendsResource,
                  'users_friends/')
ee.__i(api_)
api_.add_resource(chats_resource.ChatsListResource, 'chats')
api_.add_resource(chats_resource.ChatsResource, 'chats/')
api_.add_resource(messages_resource.MessagesResource, 'messages/')
api_.add_resource(messages_resource.MessagesListResource,
                  'messages')
api_.add_resource(tokens_resource.TokensResource, 'tokens/')
