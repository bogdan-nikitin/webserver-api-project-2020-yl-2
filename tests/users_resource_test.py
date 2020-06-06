from requests import post, get, put

from tests.paths import *

print(post(USERS_URL,
           json={'first_name': 'test_first',
                 'second_name': 'test_second',
                 'password': 'test',
                 'email': 'test1@gmail.com'}).json())

"""Для тестирования последующих методов понадобится токен"""

access_token = post(LOGIN_URL,
                    json={'email': 'test@gmail.com',
                          'password': 'test',
                          'expires_in': 9999999}).json()['access_token']

wrong_token = 'wrong'

print(post(USERS_URL).json())

user = get(USERS_URL,
           json={'access_token': access_token}).json()
print(user)

user_id = user['user']['user_id']

print(get(urllib.parse.urljoin(USERS_URL, user_id)).json())

print(get(USERS_URL,
          json={'access_token': wrong_token}).json())

print(put(USERS_URL,
          json={'first_name': 'test_first_edited',
                'old_password': 'test',
                'email': 'test@gmail.com',
                'access_token': access_token}).json())

print(put(USERS_URL,
          json={'first_name': 'test_first_edited',
                'access_token': wrong_token}).json())

print(put(USERS_URL,
          json={'first_name': 'test_first_edited',
                'old_password': 'wrong_password',
                'email': 'test@gmail.com',
                'access_token': access_token}).json())

print(put(USERS_URL,
          json={'first_name': 'test_first_edited',
                'password': 'new_password',
                'email': 'test@gmail.com',
                'access_token': access_token}).json())

print(get(USERS_LIST_URL).json())

print(get(USERS_LIST_URL,
          json={'limit': 21}).json())

print(get(USERS_LIST_URL,
          json={'search_request': 'test_first'}).json())
# Данный тип запроса ещё не реализован
# print(
#     delete(USERS_URL,
#            params={'user_id': user_id, 'access_token': access_token}).json()
# )
