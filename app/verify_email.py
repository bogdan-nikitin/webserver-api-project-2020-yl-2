import hashlib
from flask import current_app


def create_token(email, created_date):
    """Создаёт токен для подтверждения email пользователя для текущего
    приложения."""
    secret_key = current_app.config['SECRET_KEY']
    # Создаём хэш, используя алгоритм SHA256, который будем использовать как
    # токен для подтверждения email пользователя
    hash_object = hashlib.sha256(bytes(email + secret_key + str(created_date),
                                       encoding='utf-8'))
    return hash_object.hexdigest()
