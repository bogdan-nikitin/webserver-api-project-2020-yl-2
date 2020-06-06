from requests import post
from tests.paths import *

"""Для тестирования нужно создать объект класса Users"""

first_name = 'auth_first'
second_name = 'auth_second'
email = 'auth_first@gmail.com'
password = 'test'

post(USERS_URL,
     json={'first_name': first_name,
           'second_name': second_name,
           'password': password,
           'email': email})

"""Тесты auth_resource"""

print(post(LOGIN_URL,
           json={'email': 'wrong_email',
                 'password': password,
                 'expires_in': 1000000}).json())

print(post(LOGIN_URL,
           json={'email': email,
                 'password': 'wrong_password',
                 'expires_in': 1000000}).json())

print(post(LOGIN_URL,
           json={'email': email,
                 'password': password,
                 'expires_in': 9999999999999999999999}).json())

true_request = post(LOGIN_URL,
                    json={'email': email,
                          'password': password,
                          'expires_in': 1000000}).json()

print(true_request)
refresh_token = true_request['refresh_token']

print(post(REFRESH_URL,
           json={'refresh_token': refresh_token}).json())
