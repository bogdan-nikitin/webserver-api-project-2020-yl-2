from requests import get, post, delete
from tests.paths import *

"""Для тестирвоания данного ресурса необходимо
добавить хотябы 2 объекта класса Users"""

post(USERS_URL,
     json={'first_name': 'friend_first',
           'second_name': 'test',
           'password': 'test',
           'email': 'friend_first@gmail.com'})

post(USERS_URL,
     json={'first_name': 'friend_second',
           'second_name': 'test',
           'password': 'test',
           'email': 'friend_second@gmail.com'})

"""Также понадобятся токены и alternative_id каждого пользователя"""

access_token_1 = post(LOGIN_URL,
                      json={'email': 'friend_first@gmail.com',
                            'password': 'test',
                            'expires_in': 9999999}).json()['access_token']

access_token_2 = post(LOGIN_URL,
                      json={'email': 'friend_second@gmail.com',
                            'password': 'test',
                            'expires_in': 9999999}).json()['access_token']

alt_id_1 = get(USERS_URL,
               json={'access_token': access_token_1}).json()['user']['user_id']

alt_id_2 = get(USERS_URL,
               json={'access_token': access_token_2}).json()['user']['user_id']

"""Тесты users_friends_resource"""

print(post(USERS_FRIENDS_URL,
           json={'friend_id': alt_id_2,
                 'action': 'add',
                 'access_token': access_token_1}).json())

print(post(USERS_FRIENDS_URL,
           json={'friend_id': alt_id_1,
                 'action': 'accept',
                 'access_token': access_token_2}).json())

print(delete(USERS_FRIENDS_URL,
             json={'friend_id': alt_id_2,
                   'access_token': access_token_1}).json())

print(post(USERS_FRIENDS_URL,
           json={'friend_id': alt_id_1,
                 'action': 'add',
                 'access_token': access_token_2}).json())

print(post(USERS_FRIENDS_URL,
           json={'friend_id': alt_id_2,
                 'action': 'deny',
                 'access_token': access_token_1}).json())

print(delete(USERS_FRIENDS_URL,
             json={'friend_id': alt_id_1,
                   'access_token': access_token_2}).json())

print(post(USERS_FRIENDS_URL,
           json={'friend_id': alt_id_2,
                 'action': 'add',
                 'access_token': access_token_1}).json())

print(post(USERS_FRIENDS_URL,
           json={'friend_id': alt_id_1,
                 'action': 'accept',
                 'access_token': access_token_2}).json())

print(get(USERS_FRIENDS_LIST_URL,
          json={'access_token': access_token_1}).json())

print(post(USERS_FRIENDS_URL,
           json={'friend_id': alt_id_1,
                 'action': 'add',
                 'access_token': access_token_2}).json())

print(get(USERS_FRIENDS_LIST_URL,
          json={'access_token': access_token_1,
                'type': 'incoming'}).json())

print(post(USERS_FRIENDS_URL,
           json={'friend_id': alt_id_2,
                 'action': 'add',
                 'access_token': access_token_1}).json())

print(get(USERS_FRIENDS_LIST_URL,
          json={'access_token': access_token_1,
                'type': 'outgoing'}).json())
