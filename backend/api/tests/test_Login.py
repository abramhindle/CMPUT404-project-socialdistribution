from django.test import TestCase
from rest_framework.test import RequestsClient


class LoginTestCase(TestCase):
    client = RequestsClient()
    username = "test123"
    password = "pw123"

    def setUp(self):
        self.client.post('http://localhost:8000/api/auth/register/',
                         data={"username": self.username, "password": self.password}
                         )

    def test_login_success(self):
        response = self.client.post('/api/auth/login/',
                                    data={"username": self.username, "password": self.password}
                                    )
        assert(response.status_code == 200)

    def test_login_fail(self):
        invalidUsername = "abcd"
        invalidPassword = "abcd"
        response = self.client.post('/api/auth/login/',
                                    data={"username": invalidUsername, "password": invalidPassword}
                                    )
        assert (response.status_code != 200)
