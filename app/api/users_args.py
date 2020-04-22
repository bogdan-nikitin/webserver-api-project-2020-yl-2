from flask_restful import reqparse


parser = reqparse.RequestParser()
parser.add_argument('first_name', required=True)
parser.add_argument('second_name', required=True)
parser.add_argument('password', required=True)
parser.add_argument('password_again', required=True)
parser.add_argument('email', required=True)
parser.add_argument('phone_number')
parser.add_argument('age', type=int)
parser.add_argument('additional_inf')
parser.add_argument('city')
parser.add_argument('avatar')


parser_edit = reqparse.RequestParser()
parser_edit.add_argument('first_name')
parser_edit.add_argument('second_name')
parser_edit.add_argument('email')
parser_edit.add_argument('phone_number')
parser_edit.add_argument('age', type=int)
parser_edit.add_argument('additional_inf')
parser_edit.add_argument('city')
parser_edit.add_argument('avatar')
