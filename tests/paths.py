import urllib.parse
API_URL = 'http://localhost:5000/api/v1/'
USERS_URL = urllib.parse.urljoin(API_URL, 'users/')
USERS_LIST_URL = urllib.parse.urljoin(API_URL, 'users')
LOGIN_URL = urllib.parse.urljoin(API_URL, 'login/')
REFRESH_URL = urllib.parse.urljoin(API_URL, 'refresh/')
CHATS_URL = urllib.parse.urljoin(API_URL, 'chats/')
CHATS_LIST_URL = urllib.parse.urljoin(API_URL, 'chats')
MESSAGES_URL = urllib.parse.urljoin(API_URL, 'messages/')
MESSAGES_LIST_URL = urllib.parse.urljoin(API_URL, 'messages')
USERS_FRIENDS_URL = urllib.parse.urljoin(API_URL, 'users_friends/')
USERS_FRIENDS_LIST_URL = urllib.parse.urljoin(API_URL, 'users_friends')
TOKENS_URL = urllib.parse.urljoin(API_URL, 'tokens/')
