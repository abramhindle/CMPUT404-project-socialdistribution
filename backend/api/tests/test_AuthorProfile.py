
from django.test import TestCase
from rest_framework.test import RequestsClient


class AuthorProfileCase(TestCase):
    client = RequestsClient()
    username = "test123"
    password = "pw123"

    def setUp(self):
        # create user
        response = self.client.post('http://localhost:8000/api/auth/register/',
                                    data={"username": self.username, "password": self.password}
                                    )
        self.assertEqual(response.status_code, 200)
        self.client.login(username=self.username, password=self.password)

    def test_AuthorProfile(self):
        github_link = "https://github.com/forgeno/"
        response = self.client.post('/api/profile/', {"github": github_link})
        self.assertEqual(response.status_code, 200)

