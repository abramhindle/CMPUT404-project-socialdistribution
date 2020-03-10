import json
from pprint import pprint
from django.test import TestCase, RequestFactory
from django.shortcuts import render
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from user.models import User
from friend.models import Friend
from .models import Post
from .views import PostsViewSet


class PostTestCase(APITestCase):
    def setUp(self):
        """
        setup user1, user2, user3, user4
        setup post1 by user1,  post2 by user2, post3 by user3, post4 by user4
        setup friend(user1, user2) friend(user2, user3)
        """
        self.user1 = User.objects.create_user(
            email="user1@email.com", username="user1", password="passqweruser1",
        )
        self.token1 = Token.objects.create(user=self.user1)

        self.user2 = User.objects.create_user(
            email="user2@email.com", username="user2", password="passqweruser2",
        )
        self.token2 = Token.objects.create(user=self.user2)

        self.user3 = User.objects.create_user(
            email="user3@email.com", username="user3", password="passqweruser3",
        )
        self.token3 = Token.objects.create(user=self.user3)

        self.user4 = User.objects.create_user(
            email="user4@email.com", username="user4", password="passqweruser4",
        )
        self.token4 = Token.objects.create(user=self.user4)

        self.post1 = Post.objects.create(
            title="post1",
            content="this post1 from user1",
            author=self.user1,
            visibility="PUBLIC",
        )
        self.post2 = Post.objects.create(
            title="post2",
            content="this post2 from user2",
            author=self.user2,
            visibility="FRIENDS",
        )
        self.post3 = Post.objects.create(
            title="post3",
            content="this post3 from user3",
            author=self.user3,
            visibility="FOAF",
        )
        self.post4 = Post.objects.create(
            title="post4",
            content="this post4 from user4",
            author=self.user4,
            visibility="PUBLIC",
        )
        Friend.objects.create(f1Id=self.user1, f2Id=self.user2, status="A")
        Friend.objects.create(f1Id=self.user2, f2Id=self.user3, status="A")

    def test_create_post(self):
        request_body = {
            "title": "test post",
            "content": "test post content",
        }

        response = self.client.post(
            "/api/post/", request_body, HTTP_AUTHORIZATION="Token " + self.token4.key,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post("/api/post/", request_body,)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        del request_body["title"]
        response = self.client.post(
            "/api/post/", request_body, HTTP_AUTHORIZATION="Token " + self.token4.key,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_post(self):
        response = self.client.get("/api/post/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(f"/api/post/{str(self.post1.id)}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(f"/api/post/{str(self.post2.id)}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.get(
            f"/api/post/{str(self.post2.id)}/",
            HTTP_AUTHORIZATION="Token " + self.token1.key,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(
            f"/api/post/{str(self.post2.id)}/",
            HTTP_AUTHORIZATION="Token " + self.token4.key,
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.get(f"/api/post/{str(self.post3.id)}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.get(
            f"/api/post/{str(self.post3.id)}/",
            HTTP_AUTHORIZATION="Token " + self.token1.key,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(
            f"/api/post/{str(self.post3.id)}/",
            HTTP_AUTHORIZATION="Token " + self.token2.key,
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.get(
            f"/api/post/{str(self.post3.id)}/",
            HTTP_AUTHORIZATION="Token " + self.token4.key,
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_post(self):
        request_body = {
            "content": self.post1.content + " updated",
        }

        response = self.client.patch(
            f"/api/post/{str(self.post1.id)}/",
            request_body,
            HTTP_AUTHORIZATION="Token " + self.token4.key,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.patch(
            f"/api/post/{str(self.post1.id)}/",
            request_body,
            HTTP_AUTHORIZATION="Token " + self.token1.key,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_post(self):
        response = self.client.delete(
            f"/api/post/{str(self.post4.id)}/",
            HTTP_AUTHORIZATION="Token " + self.token1.key,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete(
            f"/api/post/{str(self.post4.id)}/",
            HTTP_AUTHORIZATION="Token " + self.token4.key,
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_timeline_post(self):
        response = self.client.get(
            f"/api/user/author/{self.user1.username}/user_posts/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
