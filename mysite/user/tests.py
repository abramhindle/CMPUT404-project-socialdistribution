import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from .models import User


class UserTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user1@email.com", username="user1", password="passqweruser1",
        )
        self.token = Token.objects.create(user=self.user)

    def test_create_user(self):
        request_1_body = {
            "username": "user2",
            "email": "user2@email.com",
            "password1": "passqweruser2",
            "password2": "passqweruser2",
        }
        response = self.client.post("/api/user/signup/", request_1_body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # user1 created

        request_2_body = {
            "email": request_1_body["email"],
            "password": request_1_body["password1"],
        }
        response = self.client.post("/api/user/login/", request_2_body)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_username_conflict(self):
        request_body = {
            "username": self.user.username,
            "email": self.user.email,
            "password1": self.user.password,
            "password2": self.user.password,
        }
        response = self.client.post("/api/user/signup/", request_body)
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )  # user1 existed

    def test_list_user(self):
        response = self.client.get("/api/user/author/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_user(self):
        response = self.client.get("/api/user/author/user1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.render()
        data = json.loads(json.dumps(response.data))
        self.assertEqual(data["email"], self.user.email)

    def test_update_user(self):
        request_body = {
            "bio": "Hi, I am user1",
        }
        response = self.client.patch(
            "/api/user/author/user1/",
            request_body,
            HTTP_AUTHORIZATION="Token " + self.token.key,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.render()
        data = json.loads(json.dumps(response.data))
        self.assertEqual(data["bio"], request_body["bio"])

    def test_delete_user(self):
        response = self.client.delete(
            "/api/user/author/user1/", HTTP_AUTHORIZATION="Token " + self.token.key,
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
