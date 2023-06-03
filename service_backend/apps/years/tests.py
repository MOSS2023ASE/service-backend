from service_backend.apps.years.models import Year
from rest_framework.test import APITestCase


# Create your tests here.
class YearAPITestCase(APITestCase):
    def setUp(self):
        year = Year(id=1, content='test1')
        year.save()
        year = Year(id=2, content='test2')
        year.save()

    def test_list(self):
        url = '/year/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']['year_list']), 2)
        return

    def test_create(self):
        url = '/year/create'
        data = {"content": "test_content"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['success'], True)
        self.assertEqual(response.data['code'], 0)
        self.assertEqual(response.data['message'], 'create year success!')
        return

    def test_update(self):
        url = '/year/update'
        data = {
            "year_id": 1,
            "content": "test_update"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], "update year success!")
        return

    def test_delete(self):
        url = '/year/delete'
        data = {
            "year_id": 2
        }
        response = self.client.delete(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], "delete year success!")
        return

    def test_current_year(self):
        url = '/year/update_current'
        data = {
            "year_id": 1,
            "content": "当前学年"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)