from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import RequestsClient
from ..models import Category, Post, AuthorProfile, Follow, Comment
from ..serializers import PostSerializer, AuthorProfileSerializer, CommentSerializer
import json
import time
from .util import *
from django.conf import settings

class CommentTestCase(TestCase):
    client = RequestsClient()
    username1 = "test123"
    password1 = "pw123"
    username2 = "test234"
    password2 = "pw234"
    host = settings.BACKEND_URL

    def setUp(self):
        self.user1 = User.objects.create_user(username=self.username1, password=self.password1)
        self.user2 = User.objects.create_user(username=self.username2, password=self.password2)
        self.authorProfile1 = AuthorProfile.objects.create(
                                                        host=self.host,
                                                        displayName="Lara Croft",
                                                        github="http://github.com/laracroft",
                                                        user=self.user1)

        self.authorProfile2 = AuthorProfile.objects.create(
                                                    host=self.host,
                                                    displayName="Lara Croft2",
                                                    github="http://github.com/laracroft2",
                                                    user=self.user2)
        self.user_id_1 = get_author_id(self.authorProfile1.host, self.authorProfile1.id, False)

        self.public_post1 = {
            "title": "A post title about a post about web dev",
            "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
            "origin": "http://whereitcamefrom.com/posts/zzzzz",
            "description": "This post discusses stuff -- brief",
            "contentType": "text/plain",
            "content": "public_post content",
            "categories": ["test_category_1", "test_category_2"],
            "published": "2015-03-09T13:07:04+00:00",
            "visibility": "PUBLIC",
            "visibleTo": [],
            "unlisted": False
                    }

    # def test_invalid_auth(self):
    #     response = self.client.get("/api/author/posts")
    #     self.assertEqual(response.status_code, 403)

    def test_comment_on_author_post(self):
        Post.objects.all().delete()
        Follow.objects.all().delete()

        self.client.login(username=self.username2, password=self.password2)
        mock_post = create_mock_post(self.public_post1, self.authorProfile1)
        response = self.client.post("/api/posts/{}/comments".format(mock_post.id),
                                        data={
                                            "comment": "What a wonderful test comment",
                                            "contentType": "text/plain"
                                        },
                                        content_type="application/json")

        time.sleep(0.0001)

        self.client.post("/api/posts/{}/comments".format(mock_post.id),
                                        data={
                                            "comment": "Gundam Wing",
                                            "contentType": "text/plain"
                                        },
                                        content_type="application/json")

        self.assertEqual(response.status_code, 200)
        response_obj = {
            "query": "addComment",
            "success": True,
            "message":"Comment Added"
        }
        self.assertEqual(response.data, response_obj)

        response = self.client.get("/api/author/{}/posts".format(self.authorProfile1.id))
        expected_output = {
            "query": "posts",
            "count": 1,
            "posts": [self.public_post1]
        }

        expected_comment_info = {
            "commenting_authors": [self.authorProfile2, self.authorProfile2],
            "contentType": ["text/plain", "text/plain"],
            "comments": ["Gundam Wing", "What a wonderful test comment"]
        }

        expected_author_list = [self.authorProfile1]
        assert_post_response(response, expected_output, expected_author_list)
        assert_comments(response.data["posts"][0]["comments"], self.authorProfile2, expected_comment_info)

    def test_comment_private_post(self):
        self.client.login()
        private_post = self.public_post1.copy()
        private_post["visibility"] = "PRIVATE"
        
        self.client.login(username=self.username2, password=self.password2)
        mock_post = create_mock_post(private_post, self.authorProfile1)
        response = self.client.post("/api/posts/{}/comments".format(mock_post.id),
                                        data={
                                            "comment": "What a wonderful test comment",
                                            "contentType": "text/plain"
                                        },
                                        content_type="application/json")
        self.assertEqual(response.status_code, 403)                                    
