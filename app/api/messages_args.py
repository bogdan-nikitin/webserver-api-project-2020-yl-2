from flask_restful import reqparse


parser = reqparse.RequestParser()
parser.add_argument('sender_id', required=True, type=int)
parser.add_argument('chat_id', required=True, type=int)
parser.add_argument('text', required=True)
