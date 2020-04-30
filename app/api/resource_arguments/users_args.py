from flask_restful import reqparse


# get_parser = reqparse.RequestParser()
# get_parser.add_argument('user_id', required=False)


post_parser = reqparse.RequestParser()
post_parser.add_argument('first_name', required=True)
post_parser.add_argument('second_name', required=True)
post_parser.add_argument('password', required=True)
post_parser.add_argument('email', required=True)
post_parser.add_argument('phone_number')
post_parser.add_argument('age', type=int)
post_parser.add_argument('additional_inf')
post_parser.add_argument('city')
post_parser.add_argument('avatar')


put_parser = reqparse.RequestParser()
put_parser.add_argument('first_name')
put_parser.add_argument('second_name')
put_parser.add_argument('phone_number')
put_parser.add_argument('age', type=int)
put_parser.add_argument('additional_inf')
put_parser.add_argument('city')
put_parser.add_argument('avatar')

put_parser.add_argument('old_password')
put_parser.add_argument('email')
put_parser.add_argument('password')
