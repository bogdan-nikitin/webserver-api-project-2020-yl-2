from flask import jsonify
from flask_restful import Resource
from flask_jwt_extended import current_user, jwt_required, get_jwt_identity
from app.data import db_session
from app.data.users import Users
from app.data.users_friends import UsersFriends
from app.api.resource_arguments.users_friends_args import (
    list_get_parser, post_parser, delete_parser
)
from app.api.users_utils import (
    abort_if_not_found, USERS_PUBLIC_ONLY, USERS_PRIVATE_ONLY,
    current_user_from_db, user_by_alt_id
)
from modules.anything import anything
from modules import constants




class UsersFriendsResource(Resource):
    @jwt_required
    def post(self):
        args = post_parser.parse_args()
        abort_if_not_found(args.friend_id)
        session = db_session.create_session()
        inviter = current_user_from_db(session)
        invitee = user_by_alt_id(session, args.friend_id)
        if session.query(UsersFriends).filter(
                (UsersFriends.inviter_id == inviter.id) &
                (UsersFriends.invitee_id == invitee.id)).first():
            return jsonify({'error': 'Users already friends'})
        users_friends_obj = UsersFriends(
            inviter_id=inviter.id,
            invitee_id=invitee.id
        )
        session.add(users_friends_obj)
        session.commit()
        return jsonify({'success': 'OK'})

    # @flask_login.login_required
    def delete(self):
        args = delete_parser.parse_args()
        alt_id = args['alternative_id']
        abort_if_not_found(alt_id)
        session = db_session.create_session()
        user = session.query(Users).filter(Users.alternative_id == alt_id)
        flask_login.current_user_from_db.friends.remove(user)
        return jsonify({'success': 'OK'})


def friend_to_dict(friend):
    is_accepted = friend.is_accepted
    if is_accepted:
        only = USERS_PRIVATE_ONLY
    else:
        only = USERS_PUBLIC_ONLY
    friend_dict = friend.to_dict(only=only)
    friend_dict['is_accepted'] = is_accepted
    return friend_dict


class UsersFriendsListResource(Resource):
    @jwt_required
    def get(self):
        args = list_get_parser.parse_args()
        session = db_session.create_session()
        cur_user = current_user_from_db(session)
        is_accepted = constants.USERS_FRIENDS_LIST_RESOURCE_IS_ACCEPTED_ARG.get(
            args.is_accepted, args.is_accepted)
        friends_list = list(filter(lambda f: f.is_accepted == is_accepted,
                                   cur_user.friends))
        return jsonify({'friends': list(map(friend_to_dict, friends_list))})
        # res = []
        # for friend in cur_user.friends:
        #     users_friends_obj = session.query(UsersFriends) \
        #         .filter(((UsersFriends.invitee_id == friend.id)
        #                  | (UsersFriends.invitee_id == cur_user.id))
        #                 and ((UsersFriends.inviter_id == friend.id)
        #                      | (UsersFriends.inviter_id == cur_user.id))
        #                 and UsersFriends.is_accepted == args['is_accepted'])
        #     if users_friends_obj:
        #         res.append(friend)
        # return res

