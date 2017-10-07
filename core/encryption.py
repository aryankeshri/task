import jwt
from cryptography.fernet import Fernet
from django.conf import settings


CIPHER = Fernet(settings.SECRET_CIPHER_KEY)


def crypto_encode(value):
    """
    It take value and makes one 100 character token
    :param value: any value
    :return: token
    """
    if value == '':
        raise ValueError('Please add some value!!')
    value = str.encode(str(value))
    encrypted_text = CIPHER.encrypt(value).decode('utf-8')
    return encrypted_text


def crypto_decode(token):
    """
    It decode token to actual value
    :param token: token
    :return: it returns string value
    """
    if token == '':
        raise ValueError('Please add some value!!')
    token = str.encode(token)
    decrypted_text = CIPHER.decrypt(token)
    return decrypted_text.decode('utf-8')


def jwt_payload_handler(user):
    payload = {
        'id': crypto_encode(user.pk),
        'email': user.email,
        'role': user.role
    }
    return payload


def jwt_encode_handler(payload):
    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        'HS256'
    ).decode('utf-8')


def jwt_decode_handler(token):
    return jwt.decode(
        token,
        settings.SECRET_KEY,
        True,
        leeway=0,
        audience=None,
        issuer=None,
        algorithms=['HS256']
    )
