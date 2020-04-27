from flask_restful import reqparse


get_parser = reqparse.RequestParser()
get_parser.add_argument('is_accepted')

post_parser = reqparse.RequestParser()
post_parser.add_argument('alternative_id', required=True, type=str)

delete_parser = post_parser.copy()
