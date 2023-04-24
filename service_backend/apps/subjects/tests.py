from service_backend.apps.subjects.models import Subject
from rest_framework.test import APITestCase

from service_backend.apps.years.models import Year


# Create your tests here.
class SubjectAPITestCase(APITestCase):
    def setUp(self):
        year = Year(id=1, content="year")
        year.save()
        subject = Subject(id=1, name='subject_1', content='content_1', year=year)
        subject.save()
        subject = Subject(id=2, name='subject_2', content='content_2', year=year)
        subject.save()
        return

    def test_list(self):
        url = '/subject/'
        data = {
            "year_id": 1
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']['subject_list']), 2)
        return

    def test_create(self):
        url = '/subject/create'
        data = {
            "year_id": 1,
            "name": "subject_3",
            "content": "create_content"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['success'], True)
        self.assertEqual(response.data['message'], 'create subject success!')
        return

    def test_update(self):
        url = '/subject/update'
        data = {
            "subject_id": 1,
            "name": "update_content_test",
            "content": "update_content_test"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], "update subject success!")
        return

    def test_delete(self):
        url = '/subject/delete'
        data = {
            "subject_id": 2
        }
        response = self.client.delete(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], "delete subject success!")
        return
