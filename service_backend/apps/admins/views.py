from rest_framework.response import Response
from rest_framework.views import APIView
from service_backend.apps.users.models import User
from service_backend.apps.issues.models import Issue
from service_backend.apps.users.serializers import UserSerializer
from service_backend.apps.utils.views import response_json, encode_password, check_role
from service_backend.apps.utils.constants import UserErrorCode, UserRole, OtherErrorCode, IssueErrorCode


# Create your views here.
class CreateUser(APIView):

    @check_role([UserRole.ADMIN, ])
    def post(self, request, user_id=None):
        # create user
        try:
            student_id, name, password, role = request.data['student_id'], request.data['name'], request.data['password'], request.data['role']
            print(request.data)
            if User.objects.filter(student_id=student_id).exists():
                user = User.objects.get(student_id=student_id)
                user.name, user.password_digest, user.user_role = name, encode_password(password), role
                user.mail = user.mail if user.mail else f"{student_id}@buaa.edu.cn"
            else:
                user = User(student_id=student_id, name=name, password_digest=encode_password(password), user_role=role,
                            mail=f"{student_id}@buaa.edu.cn")
            user.save()
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=UserErrorCode.USER_SAVE_FAILED,
                message="can't save user!"
            ))
        # success
        return Response(response_json(
            success=True,
            message="create user success!"
        ))


class CreateUserBatch(APIView):

    @check_role([UserRole.ADMIN, ])
    def post(self, request, user_id=None):
        # print('user_id is:' + str(user_id))
        # preprocess list
        name_list = request.data['name_list']
        student_id_list = request.data['student_id_list']
        password_list = request.data['password_list']
        role_list = request.data['role_list']
        if len({len(name_list), len(student_id_list), len(password_list), len(role_list)}) != 1:
            return Response(response_json(
                success=False,
                code=OtherErrorCode.UNEXPECTED_JSON_FORMAT,
                message="inequal list length!"
            ))
        # iterate
        for name, student_id, password, role in zip(name_list, student_id_list, password_list, role_list):
            # create user
            try:
                if User.objects.filter(student_id=student_id).exists():
                    user = User.objects.get(student_id=student_id)
                    user.name, user.password_digest, user.user_role = name, encode_password(password), role
                    user.mail = user.mail if user.mail else f"{student_id}@buaa.edu.cn"
                else:
                    user = User(student_id=student_id, name=name, password_digest=encode_password(password), user_role=role, mail=f"{student_id}@buaa.edu.cn")
                user.save()
            except Exception as _e:
                return Response(response_json(
                    success=False,
                    code=UserErrorCode.USER_SAVE_FAILED,
                    message="can't save user!"
                ))
        # success
        return Response(response_json(
            success=True,
            message="batch create user success!"
        ))


class UserList(APIView):

    @check_role([UserRole.ADMIN, ])
    def post(self, request):
        user = User.objects.all()
        user_serializar = UserSerializer(user, many=True)
        return Response(response_json(
            success=True,
            data={
                'user_list': [
                    {
                        'user_id': user.id,
                        'student_id': user.student_id,
                        'name': user.name,
                        'user_role': user.user_role,
                        'frozen': user.frozen
                    }
                    for user in user_serializar.data
                ]
            }
        ))


class UpdateUserRole(APIView):
    @check_role([UserRole.ADMIN, ])
    def post(self, request, user_id=None):
        # get user
        try:
            user = User.objects.get(id=request.data['user_id'])
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=UserErrorCode.USER_NOT_FOUND,
                message="can't find user!"
            ))
        # modify user role
        user.user_role = request.data['user_role']
        # save user role
        try:
            user.save()
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=UserErrorCode.USER_SAVE_FAILED,
                message="can't save user!"
            ))
        return Response(response_json(
            success=True,
            message="update user role success!"
        ))


class FreezeUser(APIView):
    @check_role([UserRole.ADMIN, ])
    def post(self, request, user_id=None):
        # get user
        try:
            user = User.objects.get(id=request.data['user_id'])
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=UserErrorCode.USER_NOT_FOUND,
                message="can't find user!"
            ))
        # modify frozen status
        user.frozen = request.data['frozen']
        # save frozen status
        try:
            user.save()
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=UserErrorCode.USER_SAVE_FAILED,
                message="can't save user!"
            ))
        return Response(response_json(
            success=True,
            message="update frozen status success!"
        ))


class DeleteIssue(APIView):

    @check_role([UserRole.ADMIN, ])
    def post(self, request, user_id=None):
        try:
            issue = Issue.objects.get(id=request.data['issue_id'])
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ISSUE_NOT_FOUND,
                message="can't find issue!"
            ))
        try:
            issue.delete()
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=IssueErrorCode.ISSUE_DELETE_FAILED,
                message="can't delete issue!"
            ))
        return Response(response_json(
            success=True,
            message="delete issue success!"
        ))

