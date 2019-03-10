from django.test import TestCase
from rest_framework.test import RequestsClient
import json

from ..models import Category


class CategoryTestCase(TestCase):
    client = RequestsClient()
    username = "test123"
    password = "pw123"

    def setUp(self):
        # create user
        response = self.client.post("http://localhost:8000/api/auth/register/",
                                    data={"username": self.username, "password": self.password}
                                    )
        self.assertEqual(response.status_code, 200)

    def test_invalid_auth(self):
        # test if the endpoint is protected by auth
        response = self.client.get("/api/categories/")
        self.assertEqual(response.status_code, 403)

    def test_invalid_methods(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post("/api/categories/")
        self.assertEqual(response.status_code, 405)
        response = self.client.put("/api/categories/")
        self.assertEqual(response.status_code, 405)
        response = self.client.delete("/api/categories/")
        self.assertEqual(response.status_code, 405)
        self.client.logout()

    def test_get_categories(self):
        self.client.login(username=self.username, password=self.password)

        # test empty result
        response = self.client.get("/api/categories/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

        # test not empty result
        Category.objects.create(name="test_category_1")
        Category.objects.create(name="test_category_2")
        response = self.client.get("/api/categories/")

        expected_output = [{"name": "test_category_1"}, {"name": "test_category_2"}]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), expected_output)
        self.client.logout()
