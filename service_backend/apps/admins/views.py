from rest_framework.response import Response
from rest_framework.views import APIView
from service_backend.apps.users.models import User, Privilege
from service_backend.apps.users.serializers import UserSerializer
from service_backend.apps.utils.views import response_json, encode_password, decode_jwt
from service_backend.apps.utils.constants import UserErrorCode, UserRole


# Create your views here.
class UserCreate(APIView):
    def post(self, request):
        # check jwt
        user_id, response = decode_jwt(request['jwt'])
        if not user_id:
            return Response(response)
        # check priviledge
        privilege = Privilege(user_id=user_id)
        if not privilege or privilege.frozen or privilege.user_role != UserRole.ADMIN:
            return Response(response_json(
                success=False,
                code=UserErrorCode.PERMISSION_DENIED,
                message='permission denied!'
            ))
        # create user
        try:
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
