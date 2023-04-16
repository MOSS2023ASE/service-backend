from rest_framework.response import Response
from rest_framework.views import APIView
from service_backend.apps.users.models import User
from service_backend.apps.utils.views import response_json, encode_password, generate_jwt, check_role
from service_backend.apps.utils.constants import UserErrorCode


# Create your views here.
class UserLogin(APIView):
    def post(self, request):
        # get user
        try:
            # if no invalid id, User.objects.get will raise exception
            user = User.objects.get(student_id=request.data['student_id'])
        except Exception as e:
            return Response(
                response_json(
                    success=False,
                    code=UserErrorCode.USER_NOT_FOUND,
                    message='user not found!'
                )
            )
        # check password
        try:
            password_digest = encode_password(request.data['password'])
            if password_digest != user.password_digest:
                raise Exception()
            jwt_token = generate_jwt(user.id)
            print(jwt_token)
        except Exception as e:
            return Response(response_json(
                success=False,
                code=UserErrorCode.INCORRECT_PASSWORD,
                message='incorrect password!'
            ))
        # login success
        return Response(
            response_json(
                success=True,
                message='login success!',
                data={
                    'jwt': jwt_token
                }
            )
        )


class PasswordModify(APIView):

    @check_role([0, 1, 2])
    def post(self, request, action_user: User = None):
        if action_user.password_digest != encode_password(request.data['password_old']):
            return Response(response_json(
                success=False,
                code=UserErrorCode.INCORRECT_PASSWORD,
                message='incorrect password!'
            ))
        try:
            action_user.password_digest = encode_password(request.data['password_new'])
            action_user.save()
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=UserErrorCode.USER_SAVE_FAILED,
                message="can't save user!"
            ))
        return Response(response_json(
            success=True,
            message="modify password successfully!"
        ))


class GetUserInfo(APIView):

    @check_role([0, 1, 2])
    def post(self, request, action_user: User = None):
        return Response(response_json(
            success=True,
            message='get user information successfully!',
            data={
                'user_id': action_user.id,
                'student_id': action_user.student_id,
                'name': action_user.name,
                'mail': action_user.mail,
                'avatar': action_user.avatar
            }
        ))


class ModifyUserInfo(APIView):

    @check_role([0, 1, 2])
    def post(self, request, action_user: User = None):
        try:
            action_user.avatar = request.data['avatar']
            action_user.mail = request.data['mail']
            action_user.save()
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=UserErrorCode.USER_SAVE_FAILED,
                message="can't save user!"
            ))
        return Response(response_json(
            success=True,
            message="modify user information successfully!"
        ))


def init_database():
    user = User(student_id='20373743', name='ccy', password_digest=encode_password('123456'), user_role=2, frozen=0)
    user.save()
    user = User(student_id='20373043', name='lsz', password_digest=encode_password('123456'), user_role=0, frozen=0)
    user.save()
    user = User(student_id='20373044', name='xyy', password_digest=encode_password('123456'), user_role=1, frozen=0)
    user.save()

# init_database()
