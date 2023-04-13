from service_backend.apps.utils.constants import GlobalCode, UserErrorCode
from service_backend.settings import ENV
from datetime import datetime
from jwt import encode, decode
from hashlib import sha256


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


def encode_password(message: str, salt=ENV['PASSWORD_SALT']) -> str:
    h = sha256()
    message += salt
    h.update(message.encode())
    for i in range(1000):
        h.update(h.hexdigest())
    return h.hexdigest()
