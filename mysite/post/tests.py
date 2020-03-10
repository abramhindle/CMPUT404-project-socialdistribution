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

        self.user5 = User.objects.create_user(
            email="user5@email.com", username="user5", password="passqweruser5",
        )
        self.token5 = Token.objects.create(user=self.user5)

        self.post1 = Post.objects.create(
            title="post1",
            content="this post1 from user1",
            author=self.user1,
            visibility="FOAF",
        )
        self.post2 = Post.objects.create(
            title="post2", content="this post2 from user2", author=self.user2
        )
        self.post3 = Post.objects.create(
            title="post3", content="this post3 from user3", author=self.user3,
        )
        Friend.objects.create(f1Id=self.user1, f2Id=self.user2, status="A")
        Friend.objects.create(f1Id=self.user2, f2Id=self.user3, status="A")
        Friend.objects.create(f1Id=self.user3, f2Id=self.user4, status="A")

    def test_create_post(self):
        request_body = {
            "title": "test post",
            "content": "test post content",
        }

        response = self.client.post(
            "/api/post/", request_body, HTTP_AUTHORIZATION="Token " + self.token5.key,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post("/api/post/", request_body,)
        self.assertEqual(response.status_code, status.HTT)

    def test_update_post(self):
        pass
