from django.test import TestCase
from rest_framework.test import RequestsClient
from ..models import Category


class AuthorProfileCase(TestCase):
    client = RequestsClient()
    username = "test123"
    password = "pw123"

    def setUp(self):
        # create user
        response = self.client.post("http://localhost:8000/api/auth/register/",
                                    data={"username": self.username, "password": self.password}
                                    )
        self.assertEqual(response.status_code, 200)
        Category.objects.create(name="test_category_1")
        Category.objects.create(name="test_category_2")

    def test_get_categories(self):
        response = self.client.get("/api/categories/")
        self.assertEqual(response.status_code, 403)

        self.client.login(username=self.username, password=self.password)
        response = self.client.get("/api/categories/")
        expected_output = ["test_category_1", "test_category_2"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, expected_output)
