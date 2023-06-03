import json

from django.test import TestCase

from rest_framework.test import APITestCase


# Create your tests here.
class MailAPITestCase(APITestCase):

    def test_send_mail(self):
        url = '/mail/send'
        data = {
            "mail": "1047813474@qq.com"
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        return
