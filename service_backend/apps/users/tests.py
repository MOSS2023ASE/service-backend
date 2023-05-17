import json
from rest_framework.test import APITestCase
from service_backend.apps.users.models import User
from service_backend.apps.issues.models import Issue, ReviewIssues, AdoptIssues, LikeIssues, FollowIssues
from service_backend.apps.years.models import Year
from service_backend.apps.chapters.models import Chapter
from service_backend.apps.subjects.models import Subject, UserSubject
from service_backend.apps.utils.views import encode_password, decode_jwt


# Create your tests here.
class UserAPITestCase(APITestCase):

    def setUp(self):
        User.objects.bulk_create([
            User(id=1, student_id='20373743', name='ccy', password_digest=encode_password('123456'), user_role=2,
                 frozen=0),
            User(id=2, student_id='20373043', name='lsz', password_digest=encode_password('123456'), user_role=0,
                 frozen=0),
            User(id=3, student_id='20373044', name='xyy', password_digest=encode_password('123456'), user_role=1,
                 frozen=0),
            User(id=4, student_id='20373045', name='xxx', password_digest=encode_password('123456'), user_role=1,
                 frozen=0),
            User(id=5, student_id='20373046', name='yyy', password_digest=encode_password('123456'), user_role=1,
                 frozen=0),
            User(id=6, student_id='20373001', name='1', password_digest=encode_password('123456'), user_role=0,
                 frozen=0),
            User(id=7, student_id='20373002', name='2', password_digest=encode_password('123456'), user_role=0,
                 frozen=0),
            User(id=8, student_id='20373003', name='3', password_digest=encode_password('123456'), user_role=0,
                 frozen=0),
        ])
        Year.objects.bulk_create([Year(id=1, content='2023年')])
        Subject.objects.bulk_create([
            Subject(id=1, name='数学分析2', content='...', year_id=1),
            Subject(id=2, name='大学物理', content='...', year_id=1),
        ])
        Chapter.objects.bulk_create([
            Chapter(id=1, subject_id=1, name='多元函数求导', content='hh'),
            Chapter(id=2, subject_id=2, name='角动量', content='hhh'),
        ])
        UserSubject.objects.bulk_create([
            UserSubject(id=1, user_id=3, subject_id=1),
            UserSubject(id=2, user_id=3, subject_id=2),
        ])
        Issue.objects.bulk_create([
            Issue(id=1, title='1', content='123', user_id=1, chapter_id=1, counselor_id=4, reviewer_id=3, status=0,
                  anonymous=0, score=0),
            Issue(id=2, title='2', content='123', user_id=1, chapter_id=1, counselor_id=3, reviewer_id=4, status=0,
                  anonymous=0, score=0),
            Issue(id=3, title='3', content='123', user_id=1, chapter_id=1, counselor_id=4, reviewer_id=3, status=0,
                  anonymous=0, score=0),
            Issue(id=4, title='4', content='123', user_id=1, chapter_id=1, counselor_id=3, reviewer_id=4, status=0,
                  anonymous=0, score=0),
            Issue(id=5, title='5', content='123', user_id=1, chapter_id=1, counselor_id=4, reviewer_id=3, status=0,
                  anonymous=0, score=0)
        ])
        ReviewIssues.objects.bulk_create([
            ReviewIssues(id=1, user_id=1, reviewed_id=3, issue_id=1, status=0),
            ReviewIssues(id=2, user_id=1, reviewed_id=3, issue_id=3, status=0),
            ReviewIssues(id=3, user_id=1, reviewed_id=3, issue_id=5, status=0),
            ReviewIssues(id=4, user_id=1, reviewed_id=4, issue_id=2, status=0),
            ReviewIssues(id=5, user_id=1, reviewed_id=4, issue_id=4, status=0),
        ])
        AdoptIssues.objects.bulk_create([
            AdoptIssues(id=1, user_id=4, issue_id=1, status=0),
            AdoptIssues(id=2, user_id=4, issue_id=3, status=0),
            AdoptIssues(id=3, user_id=4, issue_id=5, status=0),
            AdoptIssues(id=4, user_id=3, issue_id=2, status=0),
            AdoptIssues(id=5, user_id=3, issue_id=4, status=0),
        ])
        FollowIssues.objects.bulk_create([
            FollowIssues(id=1, user_id=2, issue_id=1),
            FollowIssues(id=2, user_id=2, issue_id=3),
            FollowIssues(id=3, user_id=1, issue_id=5),
            FollowIssues(id=4, user_id=1, issue_id=4),
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

    def test_login_student2(self):
        url = '/user/user_login'
        data = {
            "student_id": "20373043",
            "password": "123456"
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'login success!')
        self.assertEqual(response.data['code'], 0)
        self.assertEqual(response.data['data']['role'], 0)
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

    def _student_login_6(self):
        response = self.client.post('/user/user_login', {'student_id': '20373001', 'password': '123456'})
        return response.data['data']['jwt']

    def _student_login_7(self):
        response = self.client.post('/user/user_login', {'student_id': '20373002', 'password': '123456'})
        return response.data['data']['jwt']

    def _student_login_8(self):
        response = self.client.post('/user/user_login', {'student_id': '20373003', 'password': '123456'})
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
            "avatar": "https://shieask.com/pic/20373743_20230419102933_f1c88caf-80a9-4d05-b8f2-a3d41f8fea1d.png",
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
                         "https://shieask.com/pic/20373743_20230419102933_f1c88caf-80a9-4d05-b8f2-a3d41f8fea1d.png")
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

    def test_get_review_issue1(self):
        jwt_token = self.test_login_tutor3()
        url = '/user/get_review_issue'
        data = {
            "jwt": jwt_token,
            "page_no": 1,
            "issue_per_page": 10
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], "query review issue successfully!")
        self.assertEqual(response.data['code'], 0)
        self.assertEqual(len(response.data['data']['issue_list']), 3)
        self.assertEqual({issue['issue_id'] for issue in response.data['data']['issue_list']}, {1, 3, 5})

    def test_get_review_issue2(self):
        jwt_token = self.test_login_tutor3()
        url = '/user/get_review_issue'
        data = {
            "jwt": jwt_token,
            "page_no": 1,
            "issue_per_page": 2
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], "query review issue successfully!")
        self.assertEqual(response.data['code'], 0)
        self.assertEqual(len(response.data['data']['issue_list']), 2)

    def test_get_adpot_issue1(self):
        jwt_token = self.test_login_tutor4()
        url = '/user/get_adopt_issue'
        data = {
            "jwt": jwt_token,
            "page_no": 1,
            "issue_per_page": 10
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], "query adopt issue successfully!")
        self.assertEqual(response.data['code'], 0)
        self.assertEqual(len(response.data['data']['issue_list']), 3)
        self.assertEqual({issue['issue_id'] for issue in response.data['data']['issue_list']}, {1, 3, 5})

    def test_get_adpot_issue2(self):
        jwt_token = self.test_login_tutor3()
        url = '/user/get_adopt_issue'
        data = {
            "jwt": jwt_token,
            "page_no": 1,
            "issue_per_page": 10
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], "query adopt issue successfully!")
        self.assertEqual(response.data['code'], 0)
        self.assertEqual(len(response.data['data']['issue_list']), 2)
        self.assertEqual({issue['issue_id'] for issue in response.data['data']['issue_list']}, {2, 4})

    def test_get_ask_issue1(self):
        jwt_token = self.test_login_admin()
        url = '/user/get_ask_issue'
        data = {
            "jwt": jwt_token,
            "page_no": 1,
            "issue_per_page": 10
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], "query ask issue successfully!")
        self.assertEqual(response.data['code'], 0)
        self.assertEqual(len(response.data['data']['issue_list']), 5)
        self.assertEqual({issue['issue_id'] for issue in response.data['data']['issue_list']}, {1, 2, 3, 4, 5})

    def test_get_ask_issue2(self):
        jwt_token = self.test_login_tutor3()
        url = '/user/get_ask_issue'
        data = {
            "jwt": jwt_token,
            "page_no": 1,
            "issue_per_page": 10
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], "query ask issue successfully!")
        self.assertEqual(response.data['code'], 0)
        self.assertEqual(len(response.data['data']['issue_list']), 0)

    def test_get_follow_issue1(self):
        jwt_token = self.test_login_admin()
        url = '/user/get_follow_issue'
        data = {
            "jwt": jwt_token,
            "page_no": 1,
            "issue_per_page": 10
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], "query follow issue successfully!")
        self.assertEqual(response.data['code'], 0)
        self.assertEqual(len(response.data['data']['issue_list']), 2)
        self.assertEqual({issue['issue_id'] for issue in response.data['data']['issue_list']}, {4, 5})

    def test_get_follow_issue2(self):
        jwt_token = self.test_login_student2()
        url = '/user/get_follow_issue'
        data = {
            "jwt": jwt_token,
            "page_no": 1,
            "issue_per_page": 10
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], "query follow issue successfully!")
        self.assertEqual(response.data['code'], 0)
        self.assertEqual(len(response.data['data']['issue_list']), 2)
        self.assertEqual({issue['issue_id'] for issue in response.data['data']['issue_list']}, {1, 3})

    def test_get_active_user(self):
        jwt6 = self._student_login_6()
        jwt7 = self._student_login_7()
        jwt8 = self._student_login_8()
        url = '/issue/commit'
        data_list = [
            {
                "jwt": jwt6,
                "chapter_id": 2,
                "title": "1_6",
                "content": "1st of user 6",
                "anonymous": 0
            },
            {
                "jwt": jwt6,
                "chapter_id": 2,
                "title": "2_6",
                "content": "2nd of user 6",
                "anonymous": 0
            },
            {
                "jwt": jwt7,
                "chapter_id": 2,
                "title": "1_7",
                "content": "1st of user 7",
                "anonymous": 0
            },
            {
                "jwt": jwt8,
                "chapter_id": 2,
                "title": "1_8",
                "content": "1st of user 8",
                "anonymous": 0
            },
            {
                "jwt": jwt8,
                "chapter_id": 1,
                "title": "2_8",
                "content": "2nd of user 8",
                "anonymous": 0
            },
            {
                "jwt": jwt8,
                "chapter_id": 1,
                "title": "3_8",
                "content": "3rd of user 8",
                "anonymous": 0
            },
        ]
        for data in data_list:
            self.client.post(url, data=json.dumps(data), content_type='application/json')
        url = '/user/active_users'
        data = {
            "jwt": jwt6,
            "top_k": 3
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.data['code'], 0)
        self.assertEqual(len(response.data['data']['user_list']), 3)
        self.assertEqual(response.data['data']['user_list'][0]['user_id'], 1)
        self.assertEqual(response.data['data']['user_list'][1]['user_id'], 8)
        self.assertEqual(response.data['data']['user_list'][2]['user_id'], 6)
        url = '/user/active_users'
        data = {
            "jwt": jwt7,
            "top_k": 5
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.data['code'], 0)
        self.assertEqual(len(response.data['data']['user_list']), 5)
        return
