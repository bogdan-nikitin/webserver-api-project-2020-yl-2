from flask_restful import reqparse


post_parser = reqparse.RequestParser()
post_parser.add_argument('sender_id', required=True, type=int)
post_parser.add_argument('chat_id', required=True, type=int)
post_parser.add_argument('text', required=True)
