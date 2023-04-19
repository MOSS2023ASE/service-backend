import json

from rest_framework.test import APITestCase

from service_backend.apps.chapters.models import Chapter
from service_backend.apps.issues.models import Issue, Comment
from service_backend.apps.subjects.models import Subject
from service_backend.apps.tags.models import Tag
from service_backend.apps.users.models import User
from service_backend.apps.utils.constants import IssueStatus
from service_backend.apps.utils.views import encode_password
from service_backend.apps.years.models import Year


# Create your tests here.
class IssueAPITestCase(APITestCase):
    def _student_login(self):
        response = self.client.post('/user/user_login', {'student_id': '20373043', 'password': '123456'})
        return response.data['data']['jwt']

    def _student_login_2(self):
        response = self.client.post('/user/user_login', {'student_id': '20373228', 'password': '123456'})
        return response.data['data']['jwt']

    def _tutor_login_1(self):
        response = self.client.post('/user/user_login', {'student_id': '20373044', 'password': '123456'})
        return response.data['data']['jwt']

    def _tutor_login_2(self):
        response = self.client.post('/user/user_login', {'student_id': '20373290', 'password': '123456'})
        return response.data['data']['jwt']

    def _admin_login(self):
        response = self.client.post('/user/user_login', {'student_id': '20373743', 'password': '123456'})
        return response.data['data']['jwt']

    def setUp(self):
        user = User(student_id='20373743', name='ccy', password_digest=encode_password('123456'), user_role=2, frozen=0)
        user.save()
        user = User(student_id='20373044', name='xyy', password_digest=encode_password('123456'), user_role=1, frozen=0)
        user.save()
        user = User(student_id='20373290', name='aaa', password_digest=encode_password('123456'), user_role=1, frozen=0)
        user.save()
        user = User(student_id='20373228', name='bbb', password_digest=encode_password('123456'), user_role=0, frozen=0)
        user.save()
        user = User(student_id='20373043', name='lsz', password_digest=encode_password('123456'), user_role=0, frozen=0)
        user.save()
        year = Year(content="year")
        year.save()
        subject = Subject(name='subject', content='content', year=year)
        subject.save()
        chapter = Chapter(name='chapter_1', content='content_1', subject=subject)
        chapter.save()
        chapter = Chapter(name='chapter_2', content='content_2', subject=subject)
        chapter.save()
        issue = Issue(title='issue', user=user, chapter_id=1, status=IssueStatus.NOT_ADOPT, anonymous=0)
        issue.save()
        tag = Tag(content="tag_1")
        tag.save()
        tag = Tag(content="tag_2")
        tag.save()
        comment = Comment(content="comment_1", issue=issue, user_id=1)
        comment.save()
        comment = Comment(content="comment_2", issue=issue, user=user)
        comment.save()
        return

    def test_issue_get(self):
        jwt = self._student_login()
        url = '/issue/get'
        data = {
            "jwt": jwt,
            "issue_id": 1
        }
        response = self.client.post(url, data)
        self.assertEqual(response.data['code'], 0)
        return

    def test_issue_cancel(self):
        jwt = self._student_login()
        url = '/issue/cancel'
        data = {
            "jwt": jwt,
            "issue_id": 1
        }
        response = self.client.post(url, data)
        self.assertEqual(response.data['code'], 0)
        return

    def test_issue_changes(self):
        jwt_tutor_1 = self._tutor_login_1()
        jwt_tutor_2 = self._tutor_login_2()
        jwt_student = self._student_login()
        adopt_url = '/issue/adopt'
        reject_url = '/issue/reject'
        agree_url = '/issue/agree'
        review_url = '/issue/review'
        readopt_url = '/issue/readopt'
        classify_url = '/issue/classify'
        student_data = {
            "jwt": jwt_student,
            "issue_id": 1
        }
        tutor_data_1 = {
            "jwt": jwt_tutor_1,
            "issue_id": 1
        }
        tutor_data_2 = {
            "jwt": jwt_tutor_2,
            "issue_id": 1
        }
        response = self.client.post(adopt_url, tutor_data_1)
        self.assertEqual(response.data['code'], 0)
        response = self.client.post(reject_url, student_data)
        self.assertEqual(response.data['code'], 0)
        response = self.client.post(adopt_url, tutor_data_2)
        self.assertEqual(response.data['code'], 0)
        response = self.client.post(agree_url, student_data)
        self.assertEqual(response.data['code'], 0)
        response = self.client.post(review_url, tutor_data_1)
        self.assertEqual(response.data['code'], 0)
        response = self.client.post(readopt_url, tutor_data_1)
        self.assertEqual(response.data['code'], 0)
        response = self.client.post(agree_url, student_data)
        self.assertEqual(response.data['code'], 0)
        response = self.client.post(review_url, tutor_data_2)
        self.assertEqual(response.data['code'], 0)
        tutor_data_2["is_valid"] = 0
        response = self.client.post(classify_url, json.dumps(tutor_data_2), content_type='application/json')
        self.assertEqual(response.data['code'], 0)
        return

    def test_issue_commit(self):
        jwt = self._student_login()
        url = '/issue/commit'
        data = {
            "jwt": jwt,
            "chapter_id": 1,
            "title": "issue_title",
            "content": "issue_content",
            "anonymous": 0
        }
        response = self.client.post(url, data)
        self.assertEqual(response.data['code'], 0)
        return

    def test_follow(self):
        jwt = self._student_login_2()
        follow_url = '/issue/follow'
        follow_check_url = '/issue/follow_check'
        data = {
            "jwt": jwt,
            "issue_id": 1
        }
        response = self.client.post(follow_url, data)
        self.assertEqual(response.data['code'], 0)
        response = self.client.post(follow_check_url, data)
        self.assertEqual(response.data['code'], 0)
        self.assertEqual(response.data['data']['is_follow'], 0)
        return

    def test_favorite(self):
        jwt = self._student_login_2()
        favorite_url = '/issue/favorite'
        like_url = '/issue/like'
        data = {
            "jwt": jwt,
            "issue_id": 1
        }
        response = self.client.post(favorite_url, data)
        self.assertEqual(response.data['code'], 0)
        self.assertEqual(response.data['data']['is_like'], 0)
        response = self.client.post(like_url, data)
        self.assertEqual(response.data['code'], 0)
        self.assertEqual(response.data['data']['is_like'], 1)
        response = self.client.post(favorite_url, data)
        self.assertEqual(response.data['code'], 0)
        self.assertEqual(response.data['data']['is_like'], 1)
        return

    def test_issue_update(self):
        jwt = self._student_login()
        url = '/issue/update'
        data = {
            "jwt": jwt,
            "issue_id": 1,
            "chapter_id": 1,
            "title": "test_update",
            "content": "测试更新content",
            "anonymous": 1
        }
        response = self.client.post(url, data)
        self.assertEqual(response.data['code'], 0)
        response = self.client.post('/issue/get', {"jwt": jwt, "issue_id": 1})
        self.assertEqual(response.data['code'], 0)
        return

    def test_issue_search(self):
        jwt = self._student_login()
        url = '/issue/'
        data = {
            "jwt": jwt,
            "keyword": "",
            "tag_list": [],
            "status_list": [],
            "chapter_list": [],
            "order": "",
            "page_no": 1,
            "issue_per_page": 100
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.data['code'], 0)
        return

    def test_issue_tags(self):
        jwt = self._student_login()
        url = '/issue/tags'
        data = {
            "jwt": jwt,
            "issue_id": 1
        }
        response = self.client.post(url, data)
        self.assertEqual(response.data['code'], 0)
        return

    def test_issue_tags_update(self):
        jwt = self._tutor_login_1()
        url = '/issue/tags_update'
        data = {
            "jwt": jwt,
            "issue_id": 1,
            "tag_list": [1, 2]
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.data['code'], 0)
        response = self.client.post('/issue/tags', {"jwt": jwt, "issue_id": 1})
        self.assertEqual(response.data['code'], 0)
        return

    def test_comment_list(self):
        jwt = self._student_login()
        url = '/issue/comments'
        data = {
            "jwt": jwt,
            "issue_id": 1
        }
        response = self.client.post(url, data)
        self.assertEqual(response.data['code'], 0)
        return

    def test_comment_create(self):
        jwt = self._student_login()
        url = '/issue/comment/create'
        data = {
            "jwt": jwt,
            "issue_id": 1,
            "content": "content_create"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.data['code'], 0)
        return

    def test_comment_update(self):
        jwt = self._student_login()
        url = '/issue/comment/update'
        data = {
            "jwt": jwt,
            "comment_id": 1,
            "content": "content_update"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.data['code'], 0)
        return

    def test_comment_delete(self):
        jwt = self._student_login()
        url = '/issue/comment'
        data = {
            "jwt": jwt,
            "comment_id": 1,
        }
        response = self.client.delete(url, data)
        self.assertEqual(response.data['code'], 0)
        return
