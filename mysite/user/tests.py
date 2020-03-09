import json
from pprint import pprint
from django.test import TestCase, RequestFactory
from django.shortcuts import render
from rest_framework.test import APIRequestFactory
from .models import User
from .views import AuthorViewSet


# Create your tests here.
class UserTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.factory.post(
            "/api/user/signup/",
            {
                "username": "user1",
                "email": "user1@email.com",
                "password1": "passqweruser1",
                "password2": "passqweruser2",
            },
        )

    def test_register_user(self):
        request = self.factory.get("/api/user/author/")
        response = AuthorViewSet.as_view({"get": "list"})(request, username="user1")
        response = response.render()
        print(response)
        self.assertEqual(response.status_code, 200)
        user_dict = json.loads(response.content)
        print(user_dict)
        self.assertEqual(user_dict["email"], self.user1.email)
