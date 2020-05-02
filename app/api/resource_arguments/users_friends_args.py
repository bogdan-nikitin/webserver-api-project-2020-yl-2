from flask_restful import reqparse
from modules.anything import anything
from modules import constants

list_get_parser = reqparse.RequestParser()
# list_get_parser.add_argument(
#     'is_accepted',
#     type=bool,
#     default=anything,
#     choices=constants.USERS_FRIENDS_LIST_RESOURCE_IS_ACCEPTED_ARG.keys()
# )
list_get_parser.add_argument('type',
                             choices=('incoming', 'outgoing'))

post_parser = reqparse.RequestParser()
post_parser.add_argument('friend_id', required=True, type=str)
post_parser.add_argument('action', default='add',
                         choices=('add', 'accept', 'deny'))

delete_parser = reqparse.RequestParser()
delete_parser.add_argument('friend_id', required=True, type=str)
