from service_backend.apps.utils.constants import GlobalCode, UserErrorCode
from service_backend.apps.users.models import User, BlackList
from service_backend.apps.issues.models import Issue, ReviewIssues, AdoptIssues, LikeIssues, FollowIssues
from service_backend.apps.years.models import Year
from service_backend.apps.chapters.models import Chapter
from service_backend.apps.subjects.models import Subject, UserSubject
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
        if seconds < ENV['JWT_LIFETIME'] and not BlackList.objects.filter(token=token).exists():
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
        user_id, response = decode_jwt(token)
        if not user_id:
            return Response(response)
        return f(*args, **kwargs, user_id=user_id)

    return wrapper


def check_role(role_list: list):
    def decorated(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # check jwt,  args = (<class>, <request>)
            if args[1].data.__contains__('jwt'):
                token = args[1].data['jwt']
            else:
                token = args[1].META['HTTP_TOKEN']
            user_id, response = decode_jwt(token)
            # print(user_id)
            if not user_id:
                return Response(response)
            # check authority
            user = User.objects.get(id=user_id)
            # print(user.id, user.user_role)
            if user.id and user.frozen:  # have such user and frozen
                return Response(response_json(
                    success=False,
                    code=UserErrorCode.USER_FROZEN,
                    message='your account has been frozen, please contact administrator!'
                ))
            # print(user.user_role, role_list)
            if not user.id or not (user.user_role in role_list):
                return Response(response_json(
                    success=False,
                    code=UserErrorCode.PERMISSION_DENIED,
                    message='permission denied!'
                ))
            # print(args[1].data)
            return f(*args, **kwargs, action_user=user)

        return wrapper

    return decorated


def encode_password(message: str, salt=ENV['PASSWORD_SALT']) -> str:
    h = sha256()
    message += salt
    h.update(message.encode())
    for i in range(1000):
        h.update(h.hexdigest().encode())
    return h.hexdigest()


def init_database():
    User.objects.all().delete()
    User.objects.bulk_create([
        User(student_id='20373743', name='ccy', password_digest=encode_password('123456'), user_role=2, frozen=0),
        User(student_id='20373043', name='lsz', password_digest=encode_password('123456'), user_role=0, frozen=0),
        User(student_id='20373044', name='xyy', password_digest=encode_password('123456'), user_role=1, frozen=0),
        User(student_id='20373045', name='xxx', password_digest=encode_password('123456'), user_role=1, frozen=0),
    ])
    Year.objects.all().delete()
    Year.objects.bulk_create([Year(content='2023年')])
    Subject.objects.all().delete()
    Subject.objects.bulk_create([
        Subject(name='数学分析2', content='...', year_id=1),
        Subject(name='大学物理', content='...', year_id=1),
    ])
    Chapter.objects.all().delete()
    Chapter.objects.bulk_create([
        Chapter(subject_id=1, name='多元函数求导', content='hh'),
        Chapter(subject_id=2, name='角动量', content='hhh'),
    ])
    UserSubject.objects.all().delete()
    UserSubject.objects.bulk_create([
        UserSubject(user_id=3, subject_id=1),
        UserSubject(user_id=3, subject_id=2),
    ])
    Issue.objects.all().delete()
    Issue.objects.bulk_create([
        Issue(title='1', content='123', user_id=1, chapter_id=1, counselor_id=3, reviewer_id=4, status=0, anonymous=0,
              score=0),
        Issue(title='2', content='123', user_id=1, chapter_id=1, counselor_id=3, reviewer_id=4, status=0, anonymous=0,
              score=0),
        Issue(title='3', content='123', user_id=1, chapter_id=1, counselor_id=3, reviewer_id=4, status=0, anonymous=0,
              score=0),
        Issue(title='4', content='123', user_id=1, chapter_id=1, counselor_id=3, reviewer_id=4, status=0, anonymous=0,
              score=0),
        Issue(title='5', content='123', user_id=1, chapter_id=1, counselor_id=3, reviewer_id=4, status=0, anonymous=0,
              score=0)
    ])
    ReviewIssues.objects.all().delete()
    ReviewIssues.objects.bulk_create([
        ReviewIssues(user_id=1, reviewer_id=3, issue_id=1, status=0),
        ReviewIssues(user_id=1, reviewer_id=3, issue_id=3, status=0),
        ReviewIssues(user_id=1, reviewer_id=3, issue_id=5, status=0),
        ReviewIssues(user_id=1, reviewer_id=4, issue_id=4, status=0),
    ])

# init_database()

# print(generate_jwt(10001))
