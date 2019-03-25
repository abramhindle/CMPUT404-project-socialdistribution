from django.test import TestCase
from rest_framework.test import RequestsClient


class RegisterTestCase(TestCase):
    client = RequestsClient()
    username = "test123"
    password = "pw123"

    register_input = {
        "username": "test_username",
        "password": "test_pw",
        "displayName": "test_displayname",
        "github": "https://github.com/forgeno/",
        "bio": "some bio",
        "firstName": "first-name",
        "lastName": "last-name",
        "email": "aa@gmail.com"
    }

    def test_register_empty(self):
        #test empty fields
        response = self.client.post("http://localhost:8000/api/auth/register/",
                                    data={},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        
    def test_min_register(self):
        #test successful register with minimum fields
        response = self.client.post("http://localhost:8000/api/auth/register/",
                                    data={
                                        "username": self.register_input["username"],
                                        "password": self.register_input["password"],
                                        "displayName": self.register_input["displayName"],
                                        "github": "",
                                        "bio": "",
                                        "firstName": "",
                                        "lastName": "",
                                        "email": "",},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)

        #test register with a pre-existing username
        response = self.client.post("http://localhost:8000/api/auth/register/",
                                    data={
                                        "username": self.register_input["username"],
                                        "password": self.register_input["password"],
                                        "displayName": self.register_input["displayName"],
                                        "github": "",
                                        "bio": "",
                                        "firstName": "",
                                        "lastName": "",
                                        "email": ""},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_full_register(self):
        #test successful register with all fields
        response = self.client.post("http://localhost:8000/api/auth/register/",
                                    data={
                                        "username": "aaa",
                                        "password": "bbb",
                                        "displayName": "ccc",
                                        "github": "ddd",
                                        "bio": "eee",
                                        "firstName": "fff",
                                        "lastName": "ggg",
                                        "email": "hhh"},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)