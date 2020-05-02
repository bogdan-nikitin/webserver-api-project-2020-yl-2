from flask_restful import reqparse
from modules.anything import anything
from modules import constants

list_get_parser = reqparse.RequestParser()
list_get_parser.add_argument(
    'is_accepted',
    default=anything,
    choices=constants.USERS_FRIENDS_LIST_RESOURCE_IS_ACCEPTED_ARG.keys()
)

post_parser = reqparse.RequestParser()
post_parser.add_argument('friend_id', required=True, type=str)

delete_parser = post_parser.copy()
