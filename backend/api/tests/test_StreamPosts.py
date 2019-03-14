from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client, RequestFactory
from rest_framework.test import RequestsClient
from ..models import Post, AuthorProfile, Follow, Category
from ..serializers import PostSerializer
import json
import uuid
from .util import *

class StreamPosts(TestCase):
    client = RequestsClient()
    username1 = "test123"
    password1 = "pw123"
    username2 = "test234"
    password2 = "pw234"
    username3 = "test345"
    password3 = "pw345"
    username4 = "test456"
    password4 = "pw456"
    username5 = "test567"
    password5 = "pw567"

    def setUp(self):
        self.user1 = User.objects.create_user(username=self.username1, password=self.password1)
        self.user2 = User.objects.create_user(username=self.username2, password=self.password2)
        self.user3 = User.objects.create_user(username=self.username3, password=self.password3)
        self.user4 = User.objects.create_user(username=self.username4, password=self.password4)
        self.user5 = User.objects.create_user(username=self.username5, password=self.password5)

        self.authorProfile1 = AuthorProfile.objects.create(host="http://127.0.0.1:5454/",
                                                          displayName="Lara Croft",
                                                          github="http://github.com/laracroft",
                                                          user=self.user1)

        self.authorProfile2 = AuthorProfile.objects.create(
                                                            host="http://127.0.0.1:5454/",
                                                            displayName="Lara Croft2",
                                                            github="http://github.com/laracroft2",
                                                            user=self.user2)

        self.authorProfile3 = AuthorProfile.objects.create(host="http://127.0.0.1:5454/",
                                                           displayName="Lara Croft number 3",
                                                           github="http://github.com/laracroft3",
                                                           user=self.user3)

        self.authorProfile4 = AuthorProfile.objects.create(host="http://127.0.0.1:5454/",
                                                           displayName="Lara Croft number 4",
                                                           github="http://github.com/laracroft4",
                                                           user=self.user4)

        self.authorProfile5 = AuthorProfile.objects.create(host="http://127.0.0.1:5454/",
                                                           displayName="Lara Croft number 5",
                                                           github="http://github.com/laracroft5",
                                                           user=self.user5)

        self.user_id_1 = get_author_id(self.authorProfile1.host, self.authorProfile1.id, False)
        self.user_id_2 = get_author_id(self.authorProfile2.host, self.authorProfile2.id, False)
        self.user_id_3 = get_author_id(self.authorProfile3.host, self.authorProfile3.id, False)
        self.user_id_4 = get_author_id(self.authorProfile4.host, self.authorProfile4.id, False)
        self.user_id_5 = get_author_id(self.authorProfile5.host, self.authorProfile5.id, False)

        Category.objects.create(name="test_category_1")
        Category.objects.create(name="test_category_2")

        self.public_post1 = {
            "title": "A post title about a post about web dev",
            "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
            "origin": "http://whereitcamefrom.com/posts/zzzzz",
            "description": "This post discusses stuff -- brief",
            "contentType": "text/plain",
            "content": "public_post content",
            "categories": ["test_category_1", "test_category_2"],
            "published": "2015-03-09T13:07:04+00:00",
            "id": "de305d54-75b4-431b-adb2-eb6b9e546013",
            "visibility": "PUBLIC",
            "visibleTo": [],
            "unlisted": False
                    }

        self.public_post2 = {
            "title": "A blog about the joys of TDD",
            "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
            "origin": "http://whereitcamefrom.com/posts/zzzzz",
            "description": "This post discusses stuff -- brief",
            "contentType": "text/plain",
            "content": "public_post content",
            "categories": ["test_category_1", "test_category_2"],
            "published": "2015-03-09T13:07:04+00:00",
            "id": "de305d54-75b4-431b-adb2-eb6b9e546014",
            "visibility": "PUBLIC",
            "visibleTo": [],
            "unlisted": False
                    }

        self.unlisted_post = {
            "title": "A ninja hidden in the blog",
            "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
            "origin": "http://whereitcamefrom.com/posts/zzzzz",
            "description": "This post discusses stuff -- brief",
            "contentType": "text/plain",
            "content": "public_post content",
            "categories": ["test_category_1", "test_category_2"],
            "published": "2015-03-09T13:07:04+00:00",
            "id": "de305d54-75b4-431b-adb2-eb6b9e546015",
            "visibility": "PUBLIC",
            "visibleTo": [],
            "unlisted": True
                    }

    def test_invalid_auth(self):
        response = self.client.get("/api/author/posts")
        self.assertEqual(response.status_code, 403)

    def test_get_public_post(self):
        Post.objects.all().delete()
        self.client.login(username=self.username2, password=self.password2)
        
        create_mock_post(self.public_post1, self.authorProfile1)
        create_mock_post(self.public_post2, self.authorProfile3)

        response = self.client.get("/api/author/posts")

        expected_output = {
            "query": "posts",
            "count": 2,
            "posts": [self.public_post2, self.public_post1]
        }

        expected_author_list = [self.authorProfile3, self.authorProfile1] 

        self.assertEqual(response.status_code, 200)
        assert_post_response(response, expected_output, expected_author_list)

    
    def test_get_unlisted_post(self):
        Post.objects.all().delete()
        self.client.login(username=self.username2, password=self.password2)

        create_mock_post(self.public_post1, self.authorProfile1)
        create_mock_post(self.public_post2, self.authorProfile3)
        create_mock_post(self.unlisted_post, self.authorProfile3)

        response = self.client.get("/api/author/posts")

        expected_output = {
            "query": "posts",
            "count": 2,
            "posts": [self.public_post2, self.public_post1]
        }

        expected_author_list = [self.authorProfile3, self.authorProfile1] 

        self.assertEqual(response.status_code, 200)
        assert_post_response(response, expected_output, expected_author_list)