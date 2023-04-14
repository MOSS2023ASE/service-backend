from rest_framework.response import Response
from rest_framework.views import APIView
from service_backend.apps.users.models import User, Privilege
from service_backend.apps.issues.models import Issue
from service_backend.apps.users.serializers import UserSerializer
from service_backend.apps.utils.views import response_json, encode_password, check_privilege
from service_backend.apps.utils.constants import UserErrorCode, UserRole, OtherErrorCode, IssueErrorCode


# Create your views here.
class CreateUser(APIView):

    @check_privilege([UserRole.ADMIN, ])
    def post(self, request, user_id=None):
        # create user
        try:
            # print(request.data)
            new_user = User(name=request.data['name'],
                            student_id=request.data['student_id'],
                            password_digest=encode_password(request.data['password']))
            new_user.save()
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=UserErrorCode.USER_SAVE_FAILED,
                message="can't save user!"
            ))
        # create privilege
        try:
            new_privilege = Privilege(user_id=new_user.id)
            new_privilege.save()
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=UserErrorCode.PRIVILEGE_SAVE_FAILED,
                message="can't save privilege!"
            ))
        # success
        return Response(response_json(
            success=True,
            message="create user success!"
        ))


class CreateUserBatch(APIView):

    @check_privilege([UserRole.ADMIN, ])
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
                message="inequal length of list!"
            ))
        # iterate
        for name, student_id, password, role in zip(name_list, student_id_list, password_list, role_list):
            # create user
            try:
                if User.objects.filter(student_id=student_id).exists():
                    user = User.objects.get(student_id=student_id)
                    user.name, user.password_digest = name, encode_password(password)
                else:
                    user = User(student_id=student_id, name=name, password_digest=encode_password(password))
                user.save()
            except Exception as _e:
                return Response(response_json(
                    success=False,
                    code=UserErrorCode.USER_SAVE_FAILED,
                    message="can't save user!"
                ))
            # create privilege
            try:
                if Privilege.objects.filter(user_id=user.id).exists():
                    privilege = Privilege.objects.get(user_id=user.id)
                    privilege.user_role = role
                else:
                    privilege = Privilege(user_id=user.id, user_role=role)
                privilege.save()
            except Exception as _e:
                return Response(response_json(
                    success=False,
                    code=UserErrorCode.PRIVILEGE_SAVE_FAILED,
                    message="can't save privilege!"
                ))
        # success
        return Response(response_json(
            success=True,
            message="batch create user success!"
        ))


class UserList(APIView):

    @check_privilege([UserRole.ADMIN, ])
    def post(self, request):
        pass
        # user = User.objects.all()
        # user_serializar = UserSerializer(user, many=True)
        # return Response(response_json(
        #     success=True,
        #     data={
        #         'user_list': [
        #             {
        #                 'user_id': user.id,
        #                 'student_id': user.student_id,
        #                 'name': user.name,
        #                 'user_role': 'oh my god QAQ' # TODO
        #             }
        #             for user in user_serializar.data
        #         ]
        #     }
        # ))


class UpdatePrivilege(APIView):
    @check_privilege([UserRole.ADMIN, ])
    def post(self, request, user_id=None):
        # get privilege
        try:
            privilege = Privilege.objects.get(id=request.data['user_id'])
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=UserErrorCode.USER_NOT_FOUND,
                message="can't find user!"
            ))
        # modify user role
        privilege.user_role = request.data['user_role']
        # save privilege
        try:
            privilege.save()
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=UserErrorCode.PRIVILEGE_SAVE_FAILED,
                message="can't save privilege!"
            ))
        return Response(response_json(
            success=True,
            message="update user role success!"
        ))


class FreezeUser(APIView):
    @check_privilege([UserRole.ADMIN, ])
    def post(self, request, user_id=None):
        # get privilege
        try:
            privilege = Privilege.objects.get(id=request.data['user_id'])
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=UserErrorCode.USER_NOT_FOUND,
                message="can't find user!"
            ))
        # modify frozen status
        privilege.frozen = request.data['frozen']
        # save privilege
        try:
            privilege.save()
        except Exception as _e:
            return Response(response_json(
                success=False,
                code=UserErrorCode.PRIVILEGE_SAVE_FAILED,
                message="can't save privilege!"
            ))
        return Response(response_json(
            success=True,
            message="update frozen status success!"
        ))


class DeleteIssue(APIView):

    @check_privilege([UserRole.ADMIN, ])
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

