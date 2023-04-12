from service_backend.apps.utils.constants import GlobalCode
from service_backend.settings import ENV
from datetime import datetime
from jwt import encode, decode


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


def decode_jwt(token: str) -> (int, str):
    user_id, message = None, ''
    try:
        jwt_dict = decode(jwt=token, algorithms='HS256', key=ENV['JWT_KEY'])
        start_time = datetime.fromisoformat(jwt_dict['time'])
        seconds = (datetime.now() - start_time).seconds
        if seconds < 3600.0:
            user_id = jwt_dict['user_id']
        else:
            message = 'expired jwt token!'
    except Exception as e:
        user_id, message = None, 'invalid jwt token!'
    return user_id, message


def generate_jwt(user_id: int) -> str:
    cur_time = str(datetime.now())
    token = encode(payload={'user_id': user_id, 'time': cur_time}, algorithm='HS256',
                   key=ENV['JWT_KEY'], headers={'typ': 'JWT', 'alg': 'HS256'})
    return token
