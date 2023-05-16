import json

from rest_framework.test import APITestCase

from service_backend.apps.notifications.models import Notification, NotificationReceiver
from service_backend.apps.users.models import User
from service_backend.apps.utils.views import encode_password


# Create your tests here.
class IssueAPITestCase(APITestCase):
    def _student_login(self):
        response = self.client.post('/user/user_login', {'student_id': '20373043', 'password': '123456'})
        return response.data['data']['jwt']

    def _admin_login(self):
        response = self.client.post('/user/user_login', {'student_id': '20373743', 'password': '123456'})
        return response.data['data']['jwt']

    def setUp(self):
        user = User(id=1, student_id='20373743', name='ccy', password_digest=encode_password('123456'), user_role=2, frozen=0)
        user.save()
        user = User(id=2, student_id='20373043', name='lsz', password_digest=encode_password('123456'), user_role=0, frozen=0)
        user.save()
        notification = Notification(id=1, content='1', title='11', category=1)
        notification.save()
        notification_receiver = NotificationReceiver(id=1, notification_id=1, receiver_id=2, status=0)
        notification_receiver.save()

    def test_notification_broadcast(self):
        jwt = self._admin_login()
        url = '/notification/broadcast'
        data = {
            "jwt": jwt,
            "title": "期末考试开卷",
            "content": "happy",
            "category": 1
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.data['code'], 0)
        self.assertEqual(response.data['message'], "broadcast notification successfully!")
        jwt = self._student_login()
        url = '/notification/user_receive'
        data = {
            "jwt": jwt,
            "page_no": 1,
            "notification_per_page": 10
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.data['code'], 0)
        self.assertEqual(len(response.data['data']['notification_list']), 2)
        return

    def test_notification_clear(self):
        # create
        jwt = self._admin_login()
        url = '/notification/broadcast'
        data = {
            "jwt": jwt,
            "title": "期末考试开卷",
            "content": "happy",
            "category": 1
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.data['message'], "broadcast notification successfully!")
        data = {
            "jwt": jwt,
            "title": "期末考试闭卷",
            "content": "sad",
            "category": 1
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.data['message'], "broadcast notification successfully!")
        self.assertEqual(response.data['message'], "broadcast notification successfully!")
        data = {
            "jwt": jwt,
            "title": "期末考试取消",
            "content": "very happy",
            "category": 1
        }
        # test issue number
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.data['message'], "broadcast notification successfully!")
        jwt = self._student_login()
        url = '/notification/user_receive'
        data = {
            "jwt": jwt,
            "page_no": 1,
            "notification_per_page": 10
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.data['code'], 0)
        self.assertEqual(len(response.data['data']['notification_list']), 4)
        # clear
        url = '/notification/clear_all'
        data = {
            "jwt": jwt,
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.data['code'], 0)
        # new number
        url = '/notification/user_receive'
        data = {
            "jwt": jwt,
            "page_no": 1,
            "notification_per_page": 10
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.data['code'], 0)
        self.assertEqual(len(response.data['data']['notification_list']), 0)
        return


    def test_notification_get(self):
        jwt = self._student_login()
        url = '/notification/user_receive'
        data = {
            "jwt": jwt,
            "page_no": 1,
            "notification_per_page": 10
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.data['code'], 0)
        self.assertEqual(response.data['data']['notification_list'][0]['status'], 0)
        self.assertEqual(response.data['data']['notification_list'][0]['title'], '11')
        self.assertEqual(response.data['data']['notification_list'][0]['id'], 1)
        url = '/notification/get'
        data = {
            "jwt": jwt,
            "notification_id": 1
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.data['code'], 0)
        self.assertEqual(response.data['data']['status'], 1)
        self.assertEqual(response.data['data']['title'], '11')
        return
