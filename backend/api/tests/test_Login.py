from django.test import TestCase
from rest_framework.test import RequestsClient
from django.contrib.auth.models import User

class LoginTestCase(TestCase):
    client = RequestsClient()
    username = "test123"
    password = "pw123"

    register_input = {
        "username": "login1",
        "password": "password1",
        "displayName": "test_displayname",
        "github": "https://github.com/forgeno/",
        "bio": "some bio",
        "firstName": "first-name",
        "lastName": "last-name",
        "email": "aa@gmail.com",
    }

    def setUp(self):
        User.objects.all().delete()

    def test_invalid_login(self):
        #test invalid login
        response = self.client.post("/api/auth/login/",
                                    data={
                                        "username": "invalid_username", 
                                        "password": "invalid_password"},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_success_login(self):
        #test login with valid credentials but is not approved by admin
        response = self.client.post("/api/auth/register/",
                                    data=self.register_input,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)

        response = self.client.post("/api/auth/login/",
                                    data={"username": self.register_input["username"], "password": self.register_input["password"]},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)