from rest_framework.response import Response
from rest_framework.views import APIView
from service_backend.apps.users.models import User
from service_backend.apps.subjects.models import UserSubject, Subject
from service_backend.apps.utils.views import response_json, encode_password, generate_jwt, check_role
from service_backend.apps.utils.constants import UserErrorCode, SubjectErrorCode


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


class GetUserSubject(APIView):

    @check_role([0, 1, 2])
    def post(self, request, action_user: User = None):
        # check tutor id
        try:
            tutor_id = request.data['tutor_id']
            tutor = User.objects.get(id=tutor_id)
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=UserErrorCode.USER_NOT_FOUND,
                message='user not found!',
            ))
        # get subject list
        try:
            subject_id_set = {user_subject.subject.id for user_subject in UserSubject.objects.filter(user_id=tutor_id)}
            subject_list = [Subject.objects.get(id=subject_id) for subject_id in subject_id_set]
        except:
            return Response(response_json(
                success=False,
                code=SubjectErrorCode.SUBJECT_DOES_NOT_EXIST,
                message='subject not found!',
            ))
        # return
        return Response((response_json(
            success=True,
            message="get tutor's subjects successfully!",
            data={
                'subject_list': [
                    {
                        'subject_id': subject.id,
                        'subject_name': subject.name
                    }
                    for subject in subject_list
                ]
            }
        )))


class ModifyUserSubject(APIView):

    @check_role([0, 1, 2])
    def post(self, request, action_user: User = None):
        tutor_id, subject_id_list = request.data['tutor_id'], request.data['subject_id_list']
        try:
            UserSubject.objects.filter(user_id=tutor_id).delete()
            user_subject_list = [UserSubject(user_id=tutor_id, subject_id=subject_id)
                                 for subject_id in subject_id_list]
            UserSubject.objects.bulk_create(user_subject_list)
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=SubjectErrorCode.SUBJECT_LIST_UPDATE_FAILED,
                message='subject list update failed'
            ))
        return Response(response_json(
            success=True,
            message='subject list update successfully'
        ))


class CheckUserSubject(APIView):

    @check_role([0, 1, 2])
    def post(self, request, action_user: User = None):
        tutor_id, subject_id = request.data['tutor_id'], request.data['subject_id']
        result = 1 if UserSubject.objects.filter(user_id=tutor_id, subject_id=subject_id).exists() else 0
        return Response(response_json(
            success=True,
            message='user is a tutor of this subject!' if result else 'user is not a tutor of this subject!',
            data={
                'result': result
            }
        ))
