import flask_login
from flask import jsonify
from flask_restful import Resource, abort

from app.data import db_session
from app.data.users import Users
from app.data.users_friends import UsersFriends
from app.api.resource_arguments.users_friends_args import get_parser, \
    post_parser, delete_parser


def abort_if_user_not_found_by_alt_id(alt_id):
    session = db_session.create_session()
    user = session.query(Users).filter(Users.alternative_id == alt_id)
    if not user:
        abort(404, message=f'Пользователь с alternative_id {alt_id} не найден')


class UsersFriendsResource(Resource):
    @flask_login.login_required
    def get(self):
        args = get_parser.parse_args()
        if not args['is_accepted']:
            return flask_login.current_user.friends
        res = []
        session = db_session.create_session()
        cur_user = flask_login.current_user
        for friend in cur_user.friends:
            users_friends_obj = session.query(UsersFriends) \
                .filter(((UsersFriends.invitee_id == friend.id)
                         | (UsersFriends.invitee_id == cur_user.id))
                        and ((UsersFriends.inviter_id == friend.id)
                             | (UsersFriends.inviter_id == cur_user.id))
                        and UsersFriends.is_accepted == args['is_accepted'])
            if users_friends_obj:
                res.append(friend)
        return res

    @flask_login.login_required
    def post(self):
        args = post_parser.parse_args()
        alt_id = args['alternative_id']
        abort_if_user_not_found_by_alt_id(alt_id)
        session = db_session.create_session()
        user = session.query(Users).filter(Users.alternative_id == alt_id)
        users_friends_obj = UsersFriends(
            inviter_id=flask_login.current_user.id,
            invitee_id=user.id
        )
        session.add(users_friends_obj)
        session.commit()
        return jsonify({'success': 'OK'})

    @flask_login.login_required
    def delete(self):
        args = delete_parser.parse_args()
        alt_id = args['alternative_id']
        abort_if_user_not_found_by_alt_id(alt_id)
        session = db_session.create_session()
        user = session.query(Users).filter(Users.alternative_id == alt_id)
        flask_login.current_user.friends.remove(user)
