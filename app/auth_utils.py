import datetime
import functools
import hashlib

import jwt
from flask import current_app, abort
from flask_login import current_user
from flask_socketio import disconnect

from modules import constants


def create_email_token(email, created_date):
    """Создаёт токен для подтверждения email пользователя для текущего
    приложения."""
    secret_key = current_app.config['SECRET_KEY']
    # Создаём хэш, используя алгоритм SHA256, который будем использовать как
    # токен для подтверждения email пользователя
    hash_object = hashlib.sha256(bytes(secret_key + email + str(created_date),
                                       encoding='utf-8'))
    return hash_object.hexdigest()


def create_auth_token(data: dict, live_time=constants.JWT_LIVE_TIME,
                      **encode_kwargs):
    """Функция создаёт и возвращает JWT
    :param data: Полезная нагрузка, которую следует закодировать в токене
    :param live_time: Время срока жизни токена
    :param encode_kwargs: Дополнительные именованные параметры, которые
    передадутся в функцию кодирования токена (jwt.encode)"""
    now = datetime.datetime.utcnow()
    payload = {
        'exp': now + live_time,
        'iat': now,
        **data
    }
    encoded_jwt = jwt.encode(payload, current_app.config['SECRET_KEY'],
                             **encode_kwargs)
    return encoded_jwt


def validate_auth_token(token, **decode_kwargs):
    """Функция пытается раскодировать токен и вернуть его полезную нагрузку.
    Если во время раскодирования происходит ошибка, вызывает функцию flask.abort
    с соответствующим кодом ошибки и сообщением
    :param token: JWT, который необходимо раскодировать
    :param decode_kwargs: Именнованные параметры, которые будут переданы в
    функцию раскодирования токена (jwt.decode)"""
    try:
        return decode_auth_token(token, **decode_kwargs)
    except jwt.exceptions.InvalidSignatureError:
        abort(401, 'Invalid signature')
    except jwt.exceptions.ExpiredSignatureError:
        abort(401, 'Token expired')
    except jwt.exceptions.InvalidAudienceError:
        abort(401, 'Token\'s aud claim does not match one of the expected '
                   'audience values')
    except jwt.exceptions.InvalidIssuerError:
        abort(401, 'Token’s iss claim does not match the expected issuer')
    except jwt.exceptions.InvalidIssuedAtError:
        abort(401, 'Token’s iat claim is in the future')
    except jwt.exceptions.ImmatureSignatureError:
        abort(401, 'Token’s nbf claim represents a time in the future')
    except jwt.exceptions.InvalidKeyError:
        abort(401, 'Specified key is not in the proper format')
    except jwt.exceptions.InvalidAlgorithmError:
        abort(401, 'Bad algorithm')
    except jwt.exceptions.MissingRequiredClaimError:
        abort(401, 'Claim that is required to be present is not contained in '
                   'the claimset')


def decode_auth_token(token, **decode_kwargs):
    """Функция раскодирует токен
    :param token: JWT, который необходимо раскодировать
    :param decode_kwargs: Именнованные параметры, которые будут переданы в
    функцию раскодирования токена (jwt.decode)"""
    return jwt.decode(token, current_app.config['SECRET_KEY'],
                      **decode_kwargs)


def authenticated_only(f):
    """Декоратор по типу flask_login.login_required для FlaskIO функций"""

    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)

    return wrapped
