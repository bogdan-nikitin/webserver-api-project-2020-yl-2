import time
from requests import post, get
from tests.paths import *

"""Для тестирвоания данного ресурса необходимо
добавить хотябы 2 объекта класса Users"""

post(USERS_URL,
     json={'first_name': 'mes_first',
           'second_name': 'test',
           'password': 'test',
           'email': 'mes_first@gmail.com'}).json()

post(USERS_URL,
     json={'first_name': 'mes_second',
           'second_name': 'test',
           'password': 'test',
           'email': 'mes_second@gmail.com'}).json()

"""Также понадобятся токены и alternative_id каждого пользователя"""

access_token_1 = post(LOGIN_URL,
                      json={'email': 'mes_first@gmail.com',
                            'password': 'test',
                            'expires_in': 9999999}).json()['access_token']

access_token_2 = post(LOGIN_URL,
                      json={'email': 'mes_second@gmail.com',
                            'password': 'test',
                            'expires_in': 9999999}).json()['access_token']

alt_id_1 = get(USERS_URL,
               json={'access_token': access_token_1}).json()['user']['user_id']

alt_id_2 = get(USERS_URL,
               json={'access_token': access_token_2}).json()['user']['user_id']

"""Сообщения можно отправлять только друзьям"""

print(post(MESSAGES_URL,
           json={'receiver_id': alt_id_2,
                 'text': 'test',
                 'access_token': access_token_1}).json())

"""Так что пользователей необходимо добавить в друзья друг к другу"""

post(USERS_FRIENDS_URL,
     json={'friend_id': alt_id_2,
           'action': 'add',
           'access_token': access_token_1}).json()

post(USERS_FRIENDS_URL,
     json={'friend_id': alt_id_1,
           'action': 'accept',
           'access_token': access_token_2}).json()

"""Тесты messages_resource"""

print(post(MESSAGES_URL,
           json={'access_token': access_token_1}).json())

print(post(MESSAGES_URL,
           json={'receiver_id': alt_id_2,
                 'text': 'test',
                 'access_token': access_token_1}).json())

print(get(MESSAGES_LIST_URL,
          json={'receiver_id': alt_id_2,
                'access_token': access_token_1}).json())

"""Из предыдущего запроса получим id чата"""
chat_id = get(MESSAGES_LIST_URL,
              json={
                  'receiver_id': alt_id_2,
                  'access_token': access_token_1
              }).json()['messages'][-1]['chat_id']

print(get(MESSAGES_LIST_URL,
          json={'chat_id': chat_id,
                'access_token': access_token_1}).json())

print(get(MESSAGES_LIST_URL,
          json={'receiver_id': alt_id_2,
                'date': time.time(),
                'access_token': access_token_1}).json())
