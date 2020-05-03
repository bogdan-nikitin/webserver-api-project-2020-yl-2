from flask_socketio import join_room, leave_room, send, Namespace, emit
from flask_jwt_extended import jwt_optional, jwt_required, get_jwt_identity
import requests
import flask
import urllib.parse
from app.api_utils import get_access_token


class MainNamespace(Namespace):
    @staticmethod
    @jwt_optional
    def on_connect():
        identity = get_jwt_identity()
        if identity:
            join_room(f'user_{identity}')
            response = requests.get(
                urllib.parse.urljoin(flask.current_app.config['API_SERVER'],
                                     '/api/v1/chats/'),
                json={'access_token': get_access_token()}
            )
            if response:
                if json_response := response.json():
                    if chats := json_response.get('chats'):
                        for chat in chats:
                            join_room(f'chat_{chat["id"]}')

    # @staticmethod
    # @jwt_optional
    # def on_disconnect():
    #     identity = get_jwt_identity()
    #     if identity:
    #         leave_room(identity)
