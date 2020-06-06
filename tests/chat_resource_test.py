from requests import get, post, delete
from tests.paths import *

"""Для тестирования понадобятся два экземпляра класса Users"""

first_name_1 = 'chat_first_1'
second_name_1 = 'chat_second_1'
email_1 = 'chat_first_1@gmail.com'
password_1 = 'test'

first_name_2 = 'chat_first_2'
second_name_2 = 'chat_second_2'
email_2 = 'chat_first_2@gmail.com'
password_2 = 'test'

post(USERS_URL,
     json={'first_name': first_name_1,
           'second_name': second_name_1,
           'password': password_1,
           'email': email_1})

post(USERS_URL,
     json={'first_name': first_name_2,
           'second_name': second_name_2,
           'password': password_2,
           'email': email_2})

"""Получим их alternative_id"""

access_token_1 = post(LOGIN_URL,
                      json={'email': email_1,
                            'password': password_1,
                            'expires_in': 9999999}).json()['access_token']

access_token_2 = post(LOGIN_URL,
                      json={'email': email_2,
                            'password': password_2,
                            'expires_in': 9999999}).json()['access_token']

alt_id_1 = get(USERS_URL,
               json={'access_token': access_token_1}).json()['user']['user_id']

alt_id_2 = get(USERS_URL,
               json={'access_token': access_token_2}).json()['user']['user_id']

print(post(CHATS_URL,
           json={'first_author_id': alt_id_1,
                 'second_author_id': alt_id_2,
                 'access_token': access_token_1}).json())


true_request = get(CHATS_LIST_URL,
                   json={'access_token': access_token_1}).json()
print(true_request)
chat_id = true_request['chats'][-1]['id']

print(get(CHATS_URL,
          json={'access_token': access_token_1, 'chat_with': alt_id_2}).json())
print(get(CHATS_URL,
          json={'access_token': access_token_1, 'chat_id': chat_id}).json())

print(delete(CHATS_URL,
             json={'chat_id': chat_id,
                   'access_token': access_token_1}).json())

print(post(CHATS_URL,
           json={'first_author_id': alt_id_1,
                 'second_author_id': alt_id_2,
                 'access_token': access_token_1}).json())

print(delete(CHATS_URL,
             json={'alternative_id': alt_id_2,
                   'access_token': access_token_1}).json())

print(delete(CHATS_URL,
             json={'alternative_id': 'wrong_id',
                   'access_token': access_token_1}).json())

print(get(CHATS_URL,
          json={'access_token': access_token_1}).json())
