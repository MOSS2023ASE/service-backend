import json

from django.test import TestCase

from rest_framework.test import APITestCase

from service_backend.apps.users.models import User
from service_backend.apps.utils.views import encode_password


# Create your tests here.
class MailAPITestCase(APITestCase):
    def setUp(self):
        user = User(student_id='20373228', name='yyh', password_digest=encode_password('123456'), user_role=2, frozen=0)
        user.save()

    def test_send_mail(self):
        url = '/mail/send'
        data = {
            "mail": "1047813474@qq.com"
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        return

    def test_confirm_mail(self):
        url = '/mail/confirm'
        data = {
            "student_id": 20373228,
            "mail": "20020706@buaa.edu.cn",
            "v_code": 1234,
            "password": 123456
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.data['code'], 1501)
        return
