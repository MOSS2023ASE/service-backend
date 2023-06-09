from service_backend.apps.chapters.models import Chapter
from rest_framework.test import APITestCase

from service_backend.apps.subjects.models import Subject
from service_backend.apps.years.models import Year


# Create your tests here.
class ChapterAPITestCase(APITestCase):
    def setUp(self):
        year = Year(id=1, content="year")
        year.save()
        subject = Subject(id=1, name='subject', content='content', year=year)
        subject.save()
        chapter = Chapter(id=1, name='chapter_1', content='content_1', subject=subject)
        chapter.save()
        chapter = Chapter(id=2, name='chapter_2', content='content_2', subject=subject)
        chapter.save()
        return

    def test_list(self):
        url = '/chapter/'
        data = {
            "subject_id": 1
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']['chapter_list']), 2)
        return

    def test_create(self):
        url = '/chapter/create'
        data = {
            "subject_id": 1,
            "name": "chapter_3",
            "content": "create_content"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['success'], True)
        self.assertEqual(response.data['message'], 'create chapter success!')
        return

    def test_update(self):
        url = '/chapter/update'
        data = {
            "chapter_id": 1,
            "name": "update_content_test",
            "content": "update_content_test"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], "update chapter success!")
        return

    def test_delete(self):
        url = '/chapter/delete'
        data = {
            "chapter_id": 2
        }
        response = self.client.delete(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], "delete chapter success!")
        return
