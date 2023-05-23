from django.utils import timezone

from rest_framework.response import Response
from rest_framework.views import APIView

from service_backend.apps.mail.models import MailConfirm
from service_backend.apps.users.models import User
from service_backend.apps.utils.constants import MailErrorCode, UserErrorCode
from service_backend.apps.utils.mail_helper import send_vcode, is_valid

from service_backend.apps.utils.views import response_json, encode_password


# Create your views here.
class SendMail(APIView):
    def post(self, request):
        to_mail = request.data['mail']
        vcode = send_vcode(to_mail)
        mail_confirm = MailConfirm.objects.filter(email=to_mail)
        if not is_valid(to_mail):
            return Response(response_json(
                success=False,
                code=MailErrorCode.MAIL_FORMAT_WRONG,
                message="mail format wrong!"
            ))

        if mail_confirm:
            mail_confirm = mail_confirm.first()
            mail_confirm.vcode = vcode
        else:
            mail_confirm = MailConfirm(email=to_mail, vcode=vcode)

        try:
            mail_confirm.save()
        except Exception:
            return Response(response_json(
                success=False,
                message="can't send mail!"
            ), status=404)

        return Response(response_json(
            success=True,
            message="mail send success!"
        ))


class ConfirmMail(APIView):
    def post(self, request):
        student_id = request.data['student_id']
        mail = request.data['mail']
        vcode = request.data['v_code']
        password = request.data['password']

        user = User.objects.filter(student_id=student_id)
        if not user:
            return Response(response_json(
                success=False,
                code=UserErrorCode.USER_NOT_FOUND,
                message="user not found!"
            ))
        user = user.first()

        mail_confirm = MailConfirm.objects.filter(email=mail, vcode=vcode)
        if not (mail_confirm and timezone.now() - mail_confirm.first().created_at < timezone.timedelta(minutes=20)):
            return Response(response_json(
                success=False,
                code=MailErrorCode.MAIL_CONFIRM_FAILED,
                message="invalid vcode!"
            ))

        user.password_digest = encode_password(password)
        try:
            user.save()
        except Exception:
            return Response(response_json(
                success=False,
                code=UserErrorCode.USER_SAVE_FAILED,
                message="can't change password!"
            ))

        return Response(response_json(
            success=True,
            message="change password success!"
        ))
