import json
from rest_framework.test import APITestCase
from service_backend.apps.users.models import User
from service_backend.apps.issues.models import Issue, ReviewIssues, AdoptIssues, LikeIssues, FollowIssues
from service_backend.apps.years.models import Year
from service_backend.apps.chapters.models import Chapter
from service_backend.apps.subjects.models import Subject, UserSubject
from service_backend.apps.utils.views import encode_password, decode_jwt
from service_backend.apps.utils.constants import *

# Create your tests here.
class UserAPITestCase(APITestCase):

    def setUp(self):
        User.objects.all().delete()
        User.objects.bulk_create([
            User(id=1, student_id='20373743', name='ccy', password_digest=encode_password('123456'), user_role=2,
                 frozen=0),
            User(id=2, student_id='20373043', name='lsz', password_digest=encode_password('123456'), user_role=0,
                 frozen=0),
            User(id=3, student_id='20373044', name='xyy', password_digest=encode_password('123456'), user_role=1,
                 frozen=0),
            User(id=4, student_id='20373045', name='xxx', password_digest=encode_password('123456'), user_role=1,
                 frozen=0),
        ])
        Year.objects.all().delete()
        Year.objects.bulk_create([Year(id=1, content='2023年')])
        Subject.objects.all().delete()
        Subject.objects.bulk_create([
            Subject(id=1, name='数学分析2', content='...', year_id=1),
            Subject(id=2, name='大学物理', content='...', year_id=1),
        ])
        Chapter.objects.all().delete()
        Chapter.objects.bulk_create([
            Chapter(id=1, subject_id=1, name='多元函数求导', content='hh'),
            Chapter(id=2, subject_id=2, name='角动量', content='hhh'),
        ])
        UserSubject.objects.all().delete()
        UserSubject.objects.bulk_create([
            UserSubject(id=1, user_id=3, subject_id=1),
            UserSubject(id=2, user_id=3, subject_id=2),
        ])
        Issue.objects.all().delete()
        Issue.objects.bulk_create([
            Issue(id=1, title='1', content='123', user_id=1, chapter_id=1, counselor_id=3, reviewer_id=4, status=0,
                  anonymous=0, score=0),
            Issue(id=2, title='2', content='123', user_id=1, chapter_id=1, counselor_id=3, reviewer_id=4, status=0,
                  anonymous=0, score=0),
            Issue(id=3, title='3', content='123', user_id=1, chapter_id=1, counselor_id=3, reviewer_id=4, status=0,
                  anonymous=0, score=0),
            Issue(id=4, title='4', content='123', user_id=1, chapter_id=1, counselor_id=3, reviewer_id=4, status=0,
                  anonymous=0, score=0),
            Issue(id=5, title='5', content='123', user_id=1, chapter_id=1, counselor_id=3, reviewer_id=4, status=0,
                  anonymous=0, score=0)
        ])
        ReviewIssues.objects.all().delete()
        ReviewIssues.objects.bulk_create([
            ReviewIssues(id=1, user_id=1, reviewer_id=3, issue_id=1, status=0),
            ReviewIssues(id=2, user_id=1, reviewer_id=3, issue_id=3, status=0),
            ReviewIssues(id=3, user_id=1, reviewer_id=3, issue_id=5, status=0),
            ReviewIssues(id=4, user_id=1, reviewer_id=4, issue_id=4, status=0),
        ])

    def test_login_admin(self, password="123456"):
        url = '/user/user_login'
        data = {
            "student_id": "20373743",
            "password": password
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'login success!')
        self.assertEqual(response.data['code'], 0)
        self.assertEqual(response.data['data']['role'], 2)
        self.assertTrue(decode_jwt(response.data['data']['jwt'])[0])
        return response.data['data']['jwt']

    def test_login_tutor3(self):
        url = '/user/user_login'
        data = {
            "student_id": "20373044",
            "password": "123456"
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'login success!')
        self.assertEqual(response.data['code'], 0)
        self.assertEqual(response.data['data']['role'], 1)
        self.assertTrue(decode_jwt(response.data['data']['jwt'])[0])
        return response.data['data']['jwt']

    def test_login_tutor4(self):
        url = '/user/user_login'
        data = {
            "student_id": "20373045",
            "password": "123456"
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'login success!')
        self.assertEqual(response.data['code'], 0)
        self.assertEqual(response.data['data']['role'], 1)
        self.assertTrue(decode_jwt(response.data['data']['jwt'])[0])
        return response.data['data']['jwt']

    def test_password_modify(self):
        # 1
        jwt_token = self.test_login_admin("123456")
        url = '/user/password_modify'
        data = {
            "jwt": jwt_token,
            "password_old": "123456",
            "password_new": "111111"
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'modify password successfully!')
        self.assertEqual(response.data['code'], 0)
        # login
        url2 = '/user/user_login'
        data2 = {
            "student_id": "20373743",
            "password": "111111"
        }
        response = self.client.post(url2, data=json.dumps(data2), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'login success!')
        self.assertEqual(response.data['code'], 0)
        # 3
        url = '/user/password_modify'
        data = {
            "jwt": jwt_token,
            "password_old": "111111",
            "password_new": "123456"
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'modify password successfully!')
        self.assertEqual(response.data['code'], 0)

    def test_user_info(self):
        jwt_token = self.test_login_admin("123456")
        url = '/user/modify_user_info'
        data = {
            "jwt": jwt_token,
            "avatar": "http://shieask.com/pic/20373743_20230419102933_f1c88caf-80a9-4d05-b8f2-a3d41f8fea1d.png",
            "mail": "20373743@buaa.edu.cn"
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'modify user information successfully!')
        self.assertEqual(response.data['code'], 0)
        jwt_token = self.test_login_admin("123456")
        url1 = '/user/get_user_info'
        data1 = {
            "jwt": jwt_token
        }
        response = self.client.post(url1, data1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'get user information successfully!')
        self.assertEqual(response.data['code'], 0)
        self.assertEqual(response.data['data']['user_id'], 1)
        self.assertEqual(response.data['data']['student_id'], "20373743")
        self.assertEqual(response.data['data']['name'], "ccy")
        self.assertEqual(response.data['data']['mail'], "20373743@buaa.edu.cn")
        self.assertEqual(response.data['data']['avatar'],
                         "http://shieask.com/pic/20373743_20230419102933_f1c88caf-80a9-4d05-b8f2-a3d41f8fea1d.png")
        return

    def test_user_subject(self):
        jwt_token = self.test_login_admin()
        url1 = '/user/modify_user_subject'
        data1 = {
            "jwt": jwt_token,
            "tutor_id": 4,
            "subject_id_list": [1, 2]
        }
        response = self.client.post(url1, data=json.dumps(data1), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'subject list update successfully!')
        self.assertEqual(response.data['code'], 0)
        url2 = '/user/get_user_subject'
        data2 = {
            "jwt": jwt_token,
            "tutor_id": 4,
        }
        response = self.client.post(url2, data=json.dumps(data2), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], "get tutor's subjects successfully!")
        self.assertEqual(response.data['code'], 0)
        # print(response.data['data']['subject_list'])
        self.assertEqual(len(response.data['data']['subject_list']), 2)
        url3 = '/user/check_user_subject'
        data3 = {
            "jwt": jwt_token,
            "tutor_id": 4,
            "subject_id": 2
        }
        response = self.client.post(url3, data=json.dumps(data3), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'user is a tutor of this subject!')
        self.assertEqual(response.data['code'], 0)
        self.assertEqual(response.data['data']['result'], 1)