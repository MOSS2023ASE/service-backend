from rest_framework.test import APITestCase

from service_backend.apps.chapters.models import Chapter
from service_backend.apps.subjects.models import Subject
from service_backend.apps.tags.models import Tag
from service_backend.apps.users.models import User
from service_backend.apps.utils.views import encode_password
from service_backend.apps.years.models import Year


# Create your tests here.
class IssueAPITestCase(APITestCase):
    def _student_login(self):
        response = self.client.post('/user/user_login', {'student_id': '20373043', 'password': '123456'})
        return response.data['data']['jwt']

    def _tutor_login(self):
        response = self.client.post('/user/user_login', {'student_id': '20373044', 'password': '123456'})
        return response.data['data']['jwt']

    def _admin_login(self):
        response = self.client.post('/user/user_login', {'student_id': '20373743', 'password': '123456'})
        return response.data['data']['jwt']

    def setUp(self):
        user = User(student_id='20373743', name='ccy', password_digest=encode_password('123456'), user_role=2, frozen=0)
        user.save()
        user = User(student_id='20373043', name='lsz', password_digest=encode_password('123456'), user_role=0, frozen=0)
        user.save()
        user = User(student_id='20373044', name='xyy', password_digest=encode_password('123456'), user_role=1, frozen=0)
        user.save()
        year = Year(content="year")
        year.save()
        subject = Subject(name='subject', content='content', year=year)
        subject.save()
        chapter = Chapter(name='chapter_1', content='content_1', subject=subject)
        chapter.save()
        chapter = Chapter(name='chapter_2', content='content_2', subject=subject)
        chapter.save()
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

        return
    # jwt = eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJ0aW1lIjoiMjAyMy0wNC0xOCAwNjoyNToyMi45NjU4NTcifQ.mZGfvarKaif6PNfRmtLeZ1ydwiS-4AtceGFaOj9gW3k
    # "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJ0aW1lIjoiMjAyMy0wNC0xOCAwNjoyNToyMi45NjU4NTcifQ.mZGfvarKaif6PNfRmtLeZ1ydwiS-4AtceGFaOj9gW3k"

