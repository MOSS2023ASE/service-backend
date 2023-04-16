from service_backend.apps.utils.constants import GlobalCode, UserErrorCode
from service_backend.apps.users.models import Privilege
from service_backend.settings import ENV
from rest_framework.response import Response
from datetime import datetime
from jwt import encode, decode
from hashlib import sha256
from functools import wraps


def response_json(success, code=None, message=None, data=None):
    success = not not success
    code = (GlobalCode.SUCCESS if success else GlobalCode.SYSTEM_FAILED) if code is None else code
    message = ("Success!" if success else "Failed!") if message is None else message

    return {
        'success': success,
        'code': code,
        'message': message,
        'data': data
    }


def decode_jwt(token: str) -> (int, dict):
    user_id, message, code, response = None, '', None, None
    try:
        jwt_dict = decode(jwt=token, algorithms='HS256', key=ENV['JWT_KEY'])
        start_time = datetime.fromisoformat(jwt_dict['time'])
        seconds = (datetime.now() - start_time).seconds
        if seconds < 3600.0:
            user_id = jwt_dict['user_id']
        else:
            message, code = 'expired jwt token!', UserErrorCode.EXPIRED_JWT
    except Exception as e:
        message, code = 'invalid jwt token!', UserErrorCode.INVALID_JWT
    if not user_id:
        response = response_json(success=False, code=code, message=message)
    return user_id, response




def generate_jwt(user_id: int) -> str:
    cur_time = str(datetime.now())
    token = encode(payload={'user_id': user_id, 'time': cur_time}, algorithm='HS256',
                   key=ENV['JWT_KEY'], headers={'typ': 'JWT', 'alg': 'HS256'})
    return token


def check_jwt(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = args[1].data['jwt']  # args = (<class>, <request>)
        print(type(token), token)
        user_id, response = decode_jwt(token)
        if not user_id:
            return Response(response)
        return f(*args, **kwargs, user_id=user_id)
    return wrapper


def check_privilege(role_list: list):
    def decorated(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # check jwt,  args = (<class>, <request>)
            token = args[1].data['jwt']
            user_id, response = decode_jwt(token)
            if not user_id:
                return Response(response)
            # check authority
            privilege = Privilege.objects.get(user_id=user_id)
            if privilege.id and privilege.frozen:   # have privilege and frozen
                return Response(response_json(
                    success=False,
                    code=UserErrorCode.USER_FROZEN,
                    message='your account has been frozen, please contact administrator!'
                ))
            # print(privilege.user_role, role_list)
            if not privilege.id or not (privilege.user_role in role_list):
                return Response(response_json(
                    success=False,
                    code=UserErrorCode.PERMISSION_DENIED,
                    message='permission denied!'
                ))
            return f(*args, **kwargs, user_id=user_id)
        return wrapper
    return decorated


def encode_password(message: str, salt=ENV['PASSWORD_SALT']) -> str:
    h = sha256()
    message += salt
    h.update(message.encode())
    for i in range(1000):
        h.update(h.hexdigest().encode())
    return h.hexdigest()


# print(generate_jwt(10001))
