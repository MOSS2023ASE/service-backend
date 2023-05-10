import json
from rest_framework.test import APITestCase
from service_backend.apps.users.models import User
from service_backend.apps.issues.models import Issue, ReviewIssues, AdoptIssues, LikeIssues, FollowIssues
from service_backend.apps.years.models import Year
from service_backend.apps.chapters.models import Chapter
from service_backend.apps.subjects.models import Subject, UserSubject
from service_backend.apps.utils.views import encode_password, decode_jwt


# Create your tests here.
class AdminAPITestCase(APITestCase):

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
            User(id=5, student_id='20373046', name='yyy', password_digest=encode_password('123456'), user_role=1,
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
            Issue(id=1, title='1', content='123', user_id=1, chapter_id=1, counselor_id=4, reviewer_id=3, status=0,
                  anonymous=0, score=0),
            Issue(id=2, title='2', content='123', user_id=1, chapter_id=1, counselor_id=3, reviewer_id=4, status=0,
                  anonymous=0, score=0),
            Issue(id=3, title='3', content='123', user_id=1, chapter_id=1, counselor_id=4, reviewer_id=3, status=0,
                  anonymous=0, score=0),
            Issue(id=4, title='4', content='123', user_id=1, chapter_id=1, counselor_id=3, reviewer_id=4, status=0,
                  anonymous=0, score=0),
            Issue(id=5, title='5', content='123', user_id=1, chapter_id=1, counselor_id=4, reviewer_id=3, status=0,
                  anonymous=0, score=0),
        ])
        ReviewIssues.objects.all().delete()
        ReviewIssues.objects.bulk_create([
            ReviewIssues(id=1, user_id=1, reviewed_id=3, issue_id=1, status=0),
            ReviewIssues(id=2, user_id=1, reviewed_id=3, issue_id=3, status=0),
            ReviewIssues(id=3, user_id=1, reviewed_id=3, issue_id=5, status=0),
            ReviewIssues(id=4, user_id=1, reviewed_id=4, issue_id=2, status=0),
            ReviewIssues(id=5, user_id=1, reviewed_id=4, issue_id=4, status=0),
        ])
        AdoptIssues.objects.all().delete()
        AdoptIssues.objects.bulk_create([
            AdoptIssues(id=1, user_id=4, issue_id=1, status=0),
            AdoptIssues(id=2, user_id=4, issue_id=3, status=0),
            AdoptIssues(id=3, user_id=4, issue_id=5, status=0),
            AdoptIssues(id=4, user_id=3, issue_id=2, status=0),
            AdoptIssues(id=5, user_id=3, issue_id=4, status=0),
        ])
        FollowIssues.objects.all().delete()
        FollowIssues.objects.bulk_create([
            FollowIssues(id=1, user_id=2, issue_id=1),
            FollowIssues(id=2, user_id=2, issue_id=3),
            FollowIssues(id=3, user_id=1, issue_id=5),
            FollowIssues(id=4, user_id=1, issue_id=4),
        ])

    def _admin_login(self):
        response = self.client.post('/user/user_login', {'student_id': '20373743', 'password': '123456'})
        return response.data['data']['jwt']

    def test_create_user(self):
        jwt_token = self._admin_login()
        url = '/admins/create_user'
        data = {
            'jwt': jwt_token,
            'student_id': 20373742,
            'name': 'son',
            'password': '123456789',
            'role': 2
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'create user successfully!')
        self.assertEqual(response.data['code'], 0)
        self.client.post('/user/user_login', {'student_id': '20373742', 'password': '123456789'})

    def test_create_user_batch(self):
        jwt_token = self._admin_login()
        url = '/admins/create_user_batch'
        data = {
            'jwt': jwt_token,
            'student_id_list': [20373744, 20373745],
            'name_list': ['son', 'grandson'],
            'password_list': ['123456789', '66666666'],
            'role_list': [2, 1]
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], "batch create user successfully!")
        self.assertEqual(response.data['code'], 0)
        self.client.post('/user/user_login', {'student_id': '20373744', 'password': '123456789'})
        self.client.post('/user/user_login', {'student_id': '20373745', 'password': '66666666'})

    def test_users(self):
        jwt_token = self._admin_login()
        url = '/admins/users'
        data = {
            'jwt': jwt_token
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'get user list successfully!')
        self.assertEqual(response.data['code'], 0)
        self.assertEqual({user['user_id'] for user in response.data['data']['user_list']}, {1, 2, 3, 4, 5})
        self.assertEqual({user['name'] for user in response.data['data']['user_list']}, {'ccy', 'lsz', 'xxx', 'xyy', 'yyy'})

    def test_update_user_tole(self):
        jwt_token = self._admin_login()
        url = '/admins/update_privilege'
        data = {
            'user_id': 3,
            'user_role': 0,
            'jwt': jwt_token
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], "update user role successfully!")
        self.assertEqual(response.data['code'], 0)

    def test_freeze_user(self):
            jwt_token = self._admin_login()
            url = '/admins/freeze_user'
            data = {
                'user_id': 3,
                'frozen': 1,
                'jwt': jwt_token
            }
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data['message'], "update frozen status successfully!")
            self.assertEqual(response.data['code'], 0)

    def test_issue_delete(self):
        jwt_token = self._admin_login()
        url = '/admins/issue/delete'
        data = {
            'issue_id': 3,
            'jwt': jwt_token
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], "delete issue successfully!")
        self.assertEqual(response.data['code'], 0)






