from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client, RequestFactory
from rest_framework.test import RequestsClient
from ..models import Post, AuthorProfile
from ..serializers import PostSerializer
import json
import uuid
from .util import *

class GetPostsTestCase(TestCase):
    client = RequestsClient()
    username1 = "test123"
    password1 = "pw123"
    username2 = "test234"
    password2 = "pw234"

    def setUp(self):
        self.user1 = User.objects.create_user(username=self.username1, password=self.password1)
        self.user2 = User.objects.create_user(username=self.username2, password=self.password2)

        self.authorProfile1 = AuthorProfile.objects.create(
                                                            host="http://127.0.0.1:5454/",
                                                            displayName="Lara Croft",
                                                            github="http://github.com/laracroft",
                                                            user=self.user1)

        self.authorProfile2 = AuthorProfile.objects.create(
                                                            host="http://127.0.0.1:5454/",
                                                            displayName="Lara Croft2",
                                                            github="http://github.com/laracroft2",
                                                            user=self.user2)

        self.public_post1 = {
                    "title": "A post title about a post about web dev",
                    "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
                    "origin": "http://whereitcamefrom.com/posts/zzzzz",
                    "description": "This post discusses stuff -- brief",
                    "contentType": "text/plain",
                    "content": "public_post content",
                    "author": {
                        "id": "http://127.0.0.1:5454/author/{}".format(self.authorProfile1.id),
                        "host": "http://127.0.0.1:5454/",
                        "displayName": self.authorProfile1.displayName,
                        "url": "http://127.0.0.1:5454/author/{}".format(self.authorProfile1.id),
                        "github": self.authorProfile1.github
                    },
                    "categories": [],
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
            "author": {
                "id": "http://127.0.0.1:5454/author/{}".format(self.authorProfile1.id),
                "host": "http://127.0.0.1:5454/",
                "displayName": self.authorProfile1.displayName,
                "url": "http://127.0.0.1:5454/author/{}".format(self.authorProfile1.id),
                "github": self.authorProfile1.github
            },
            "categories": [],
            "published": "2015-03-09T13:07:04+00:00",
            "id": "de305d54-75b4-431b-adb2-eb6b9e546013",
            "visibility": "PUBLIC",
            "visibleTo": [],
            "unlisted": False
                    }
        
        
        create_mock_post(self.public_post1, self.authorProfile1)
        create_mock_post(self.public_post2, self.authorProfile1)           

    def test_get_invalid_auth(self):
        response = self.client.get("/api/author/{}/posts".format(self.authorProfile1.id))
        self.assertEqual(response.status_code, 403)

    def test_get_public_posts(self):
        self.client.login(username=self.username2, password=self.password2)

        response = self.client.get("/api/author/{}/posts".format(self.authorProfile1.id))
        created_posts = Post.objects.all()

        self.assertEqual(response.status_code, 200)
        assert_post(PostSerializer(created_posts[0]).data, self.public_post1, self.authorProfile1)
        assert_post(PostSerializer(created_posts[1]).data, self.public_post2, self.authorProfile1)

    def test_get_posts_with_invalid_author_id(self):
        self.client.login(username=self.username1, password=self.password1)
        fake_uuid = uuid.uuid4()

        response = self.client.get("/api/author/{}/posts".format(fake_uuid))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), "Error: Author does not exist!")

    def test_get_private_posts(self):
        pass
