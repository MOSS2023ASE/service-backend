from rest_framework.response import Response
from rest_framework.views import APIView
from service_backend.apps.users.models import User, Privilege
from service_backend.apps.users.serializers import UserSerializer
from service_backend.apps.utils.views import response_json, encode_password, check_privilege
from service_backend.apps.utils.constants import UserErrorCode, UserRole


# Create your views here.
class UserCreate(APIView):

    @check_privilege([UserRole.ADMIN, ])
    def post(self, request, user_id=None):
        # print('user_id is:' + str(user_id))
        # create user
        try:
            # print(request.data)
            new_user = User(name=request.data['name'],
                            student_id=request.data['student_id'],
                            password_digest=encode_password(request.data['password']))
            new_user.save()
        except Exception as e:
            return Response(response_json(
                success=False,
                code=UserErrorCode.USER_SAVE_FAILED,
                message="can't save user!"
            ))
        # create privilege
        try:
            new_privilege = Privilege(user_id=new_user.id)
            new_privilege.save()
        except Exception as e:
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


class UserList(APIView):
    def post(self, request):
        user = User.objects.all()
        user_serializar = UserSerializer(user, many=True)
        return Response(response_json(
            success=True,
            data=user_serializar.data
        ))
