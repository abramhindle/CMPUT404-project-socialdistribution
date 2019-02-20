from django.test import TestCase
from rest_framework.test import RequestsClient


class LoginTestCase(TestCase):
    client = RequestsClient()
    username = "test123"
    password = "pw123"

    def test_login(self):
        #try to login as a user that does not exist
        response = self.client.post("/api/auth/login/",
                                    data={"username": self.username, "password": self.password},
                                    content_type="application/json")
        self.assertNotEqual(response.status_code, 200)

        #create user
        response = self.client.post("http://localhost:8000/api/auth/register/",
                                    data={"username": self.username, "password": self.password},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)

        #try to login again after user is registered
        response = self.client.post("/api/auth/login/",
                                    data={"username": self.username, "password": self.password},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)

