from service_backend.apps.subjects.models import Subject
from rest_framework.test import APITestCase

from service_backend.apps.tags.models import Tag
from service_backend.apps.years.models import Year
from service_backend.apps.years.serializers import YearSerializer


# Create your tests here.
class SubjectAPITestCase(APITestCase):
    def setUp(self):
        tag = Tag(id=1, content="tag_1")
        tag.save()
        tag = Tag(id=2, content="tag_2")
        tag.save()
        return

    def test_list(self):
        url = '/tag/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']['tag_list']), 2)
        return

    def test_create(self):
        url = '/tag/create'
        data = {
            "content": "create_content"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['success'], True)
        self.assertEqual(response.data['message'], 'create tag success!')
        return

    def test_update(self):
        url = '/tag/update'
        data = {
            "tag_id": 1,
            "content": "update_content_test"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], "update tag success!")
        return

    def test_delete(self):
        url = '/tag/delete'
        data = {
            "tag_id": 2
        }
        response = self.client.delete(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], "delete tag success!")
        return
