import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from http import HTTPStatus
from backend.serializers import AuthorSerializer, CommentSerializer, PostSerializer, LikeSerializer

from backend.models import Author, Post, Like, Comment, Inbox
import requests
from datetime import datetime
from django.utils.dateparse import parse_datetime
import uuid

class PostListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        uuid_list = [
            "2f91a911-850f-4655-ac29-9115822c72b5",
            "2f91a911-850f-4655-ac29-9115822c72b6",
            "2f91a911-850f-4655-ac29-9115822c72b7",
        ]
        number_of_authors = len(uuid_list)
        User.objects.bulk_create([
            User(username="LoginViewTest{}".format(idx),
            password=make_password("Margret Thatcher"),
            is_active = False if idx == 2 else True
            ) for idx in range(number_of_authors)
        ])
        authors = []
        for author_id in range(number_of_authors):
                authors.append(Author.objects.create(
                id=uuid_list[author_id],
                user=User.objects.get(username="LoginViewTest{}".format(author_id)),
                display_name="Test unit{}".format(author_id),
                url="http://127.0.0.1:8000/author/{}".format(uuid_list[author_id]),
                host="http://127.0.0.1:8000/",
            ))
        post = Post.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a9",
            url="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72b5/post/2f91a911-850f-4655-ac29-9115822c72a9",
            title="Test Title",
            source = "https://www.youtube.com/watch?v=YIJI5U0BWr0",
            origin = "https://www.django-rest-framework.org/api-guide/views/",
            description = "Test Post",
            content_type = "text/plain",
            published="2015-03-09T13:07:04+00:00",
            content = "test text",
            author = authors[0],
        )
        post = Post.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a1",
            url="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72b5/post/2f91a911-850f-4655-ac29-9115822c72a1",
            title="Test Title2",
            source = "https://www.youtube.com/watch?v=YIJI5U0BWr0",
            origin = "https://www.django-rest-framework.org/api-guide/views/",
            description = "Test Post2",
            content_type = "text/plain",
            published="2015-03-09T13:07:04+00:00",
            content = "test text2",
            author = authors[0],
        )
        post = Post.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72b1",
            url="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72b6/post/2f91a911-850f-4655-ac29-9115822c72b1",
            title="Test Title2",
            source = "https://www.youtube.com/watch?v=YIJI5U0BWr0",
            origin = "https://www.django-rest-framework.org/api-guide/views/",
            description = "Test Post3",
            content_type = "text/plain",
            published="2015-03-09T13:07:04+00:00",
            content = "test text3",
            author = authors[1],
        )
        node = Post.objects.create(
            host="http://127.0.0.1:8001/",
            auth_info = "YWxhZGRpbjpvcGVuc2VzYW1s"
        )
    def test_author_not_found(self):
        res = self.client.get("/api/author/2f91a911-850f-4655-ac29-9115822c72b5/posts/")
        self.assertEqual(res.status_code, 404)