from requests import get, post
from tests.paths import *

"""Для тестирвоания нужно создать объект класса Users"""

first_name = 'token_first'
second_name = 'token_second'
email = 'token_first@gmail.com'
password = 'test'

post(USERS_URL,
     json={'first_name': first_name,
           'second_name': second_name,
           'password': password,
           'email': email})

"""Тесты tokens_resource"""

print(get(TOKENS_URL,
          json={'email': 'wrong_email',
                'password': password}).json())

print(get(TOKENS_URL,
          json={'email': email,
                'password': 'wrong_password'}).json())

true_request = get(TOKENS_URL,
                   json={'email': email,
                         'password': password}).json()

print(true_request)
token = true_request['token']

print(post(TOKENS_URL,
           json={'token': token}).json())
