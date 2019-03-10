from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import RequestsClient
from ..models import Category, Post, AuthorProfile
from ..serializers import PostSerializer
import json


class PostTestCase(TestCase):
    client = RequestsClient()
    username = "test123"
    password = "pw123"
    input_params = {"title": "A post title about a post about web dev",
                    "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
                    "origin": "http://whereitcamefrom.com/posts/zzzzz",
                    "description": "This post discusses stuff -- brief",
                    "contentType": "text/plain",
                    "content": "Some content",
                    "categories": ["test_category_1", "test_category_2"],
                    "visibility": "PUBLIC",
                    "visibleTo": [],
                    "unlisted": False,
                    }

    def setUp(self):
        # create user
        self.user = User.objects.create_user(username=self.username, password=self.password)
        Category.objects.create(name="test_category_1")
        Category.objects.create(name="test_category_2")
        self.authorProfile = AuthorProfile.objects.create(host="http://127.0.0.1:5454/",
                                     displayName="Lara Croft",
                                     github="http://github.com/laracroft",
                                     user=self.user)


    def test_invalid_auth(self):
        # test if the endpoint is protected by auth
        response = self.client.post("/api/posts/", data=self.input_params)
        self.assertEqual(response.status_code, 403)


    def test_create_post_fail(self):
        self.client.login(username=self.username, password=self.password)

        for key in self.input_params.keys():
            if (key == "visibleTo" or key == "unlisted"):
                continue
            invalid_input = self.input_params.copy()
            # test fields is empty
            invalid_input[key] = ""
            if (key == "categories"):
                invalid_input[key] = []
            response = self.client.post("/api/posts/", data=invalid_input)
            self.assertEqual(response.status_code, 400)

            # test field is missing
            invalid_input.pop(key)
            response = self.client.post("/api/posts/", data=invalid_input)
            self.assertEqual(response.status_code, 400)

    # helper function for validating if the post is created since some attributes not possible to assert equal
    def assert_create_post(self, output, expected_post):
        for key in expected_post.keys():
            if key != "id" and key != "author" and key != "published":
                self.assertEqual(output[key], expected_post[key])
        # assert author part
        for key in ["host", "displayName", "github"]:
            self.assertEqual(output["author"][key], expected_post["author"][key])

        expected_id = "{}author/{}".format(self.authorProfile.host, self.authorProfile.id)
        self.assertEqual(output["author"]["id"], expected_id)
        self.assertEqual(output["author"]["url"], expected_id)

    def test_create_post_success(self):
        self.client.login(username=self.username, password=self.password)

        expected_post = {"title": "A post title about a post about web dev",
                         "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
                         "origin": "http://whereitcamefrom.com/posts/zzzzz",
                         "description": "This post discusses stuff -- brief",
                         "contentType": "text/plain",
                         "content": "Some content",
                         "author": {
                             "id": "http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                             "host": "http://127.0.0.1:5454/",
                             "displayName": "Lara Croft",
                             "url": "http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                             "github": "http://github.com/laracroft"
                         },
                         "categories": ["test_category_1", "test_category_2"],
                         "published": "2015-03-09T13:07:04+00:00",
                         "id": "de305d54-75b4-431b-adb2-eb6b9e546013",
                         "visibility": "PUBLIC",
                         "visibleTo": [],
                         "unlisted": False
                         }

        # test valid input with existing categories
        response = self.client.post("/api/posts/", data=self.input_params)

        created_post = Post.objects.all()[0]
        created_post = PostSerializer(created_post).data
        self.assertEqual(response.status_code, 200)
        self.assert_create_post(created_post, expected_post)
        self.assertEqual(json.loads(response.content), "Create Post Success")

        # test valid input with non-existing categories
        expected_post["categories"] = ["non_existing_category"]
        self.input_params["categories"] = ["non_existing_category"]
        response = self.client.post("/api/posts/", data=self.input_params)
        self.assertEqual(response.status_code, 200)
        created_post = Post.objects.all()[1]
        created_post = PostSerializer(created_post).data
        self.assert_create_post(created_post, expected_post)
        self.assertEqual(json.loads(response.content), "Create Post Success")
        self.client.logout()
