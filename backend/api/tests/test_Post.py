from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import RequestsClient
from ..models import Category, Post, AuthorProfile
from ..serializers import PostSerializer
import json


class AuthorProfileCase(TestCase):
    client = RequestsClient()
    username = "test123"
    password = "pw123"

    username2 = "test123_2"
    password2 = "pw123_2"
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
        self.user2 = User.objects.create_user(username=self.username2, password=self.password2)
        Category.objects.create(name="test_category_1")
        Category.objects.create(name="test_category_2")
        self.authorProfile = AuthorProfile.objects.create(host="http://127.0.0.1:5454/",
                                                          displayName="Lara Croft",
                                                          github="http://github.com/laracroft",
                                                          user=self.user)

        self.authorProfile2 = AuthorProfile.objects.create(host="http://127.0.0.1:5454/",
                                                           displayName="Lara Croft number 2",
                                                           github="http://github.com/laracroft2",
                                                           user=self.user2)

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

    # helper function for asserting a post
    def assert_post(self, output, expected_post, author_profile):
        for key in expected_post.keys():
            if key != "id" and key != "author" and key != "published":
                self.assertEqual(output[key], expected_post[key])
        # assert author part
        for key in ["host", "displayName", "github"]:
            self.assertEqual(output["author"][key], expected_post["author"][key])

        expected_id = "{}author/{}".format(author_profile.host, author_profile.id)
        self.assertEqual(output["author"]["id"], expected_id)
        self.assertEqual(output["author"]["url"], expected_id)

    def test_create_post_success(self):
        # make sure theres no existing
        Post.objects.all().delete()
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
        self.assert_post(created_post, expected_post, self.authorProfile)
        self.assertEqual(json.loads(response.content), "Create Post Success")

        # test valid input with non-existing categories
        expected_post["categories"] = ["non_existing_category"]
        self.input_params["categories"] = ["non_existing_category"]
        response = self.client.post("/api/posts/", data=self.input_params)
        self.assertEqual(response.status_code, 200)
        created_post = Post.objects.all()[1]
        created_post = PostSerializer(created_post).data
        self.assert_post(created_post, expected_post, self.authorProfile)
        self.assertEqual(json.loads(response.content), "Create Post Success")
        self.client.logout()

    # create a mock post
    def create_mock_post(self, dict_input, author_profile):
        post = Post.objects.create(title=dict_input["title"],
                                   source=dict_input["source"],
                                   origin=dict_input["origin"],
                                   description=dict_input["description"],
                                   contentType=dict_input["contentType"],
                                   content=dict_input["content"],
                                   author=author_profile,
                                   visibility=dict_input["visibility"],
                                   unlisted=dict_input["unlisted"])
        post.categories.set(dict_input["categories"])
        post.visibleTo.set(dict_input["visibleTo"
                           ])

    def test_get_post_without_id(self):
        # make sure there's no post existing
        Post.objects.all().delete()

        public_post = {"title": "A post title about a post about web dev",
                       "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
                       "origin": "http://whereitcamefrom.com/posts/zzzzz",
                       "description": "This post discusses stuff -- brief",
                       "contentType": "text/plain",
                       "content": "public_post content",
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
        self.create_mock_post(public_post, self.authorProfile)

        public_post_2 = {"title": "public_post_2 title",
                         "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
                         "origin": "http://whereitcamefrom.com/posts/zzzzz",
                         "description": "public_post_2 description",
                         "contentType": "text/plain",
                         "content": "public_post_2 content",
                         "author": {
                             "id": "http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                             "host": "http://127.0.0.1:5454/",
                             "displayName": "Lara Croft number 2",
                             "url": "http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                             "github": "http://github.com/laracroft2"
                         },
                         "categories": ["test_category_1", "test_category_2"],
                         "published": "2015-03-09T13:07:04+00:00",
                         "id": "de305d54-75b4-431b-adb2-eb6b9e546013",
                         "visibility": "PUBLIC",
                         "visibleTo": [],
                         "unlisted": False
                         }

        self.create_mock_post(public_post_2, self.authorProfile2)

        foaf_post = {"title": "foaf_post title",
                     "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
                     "origin": "http://whereitcamefrom.com/posts/zzzzz",
                     "description": "foaf_post description",
                     "contentType": "text/plain",
                     "content": "foaf_post content",
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
                     "visibility": "FOAF",
                     "visibleTo": [],
                     "unlisted": False
                     }
        self.create_mock_post(foaf_post, self.authorProfile)

        friends_post = {"title": "friends_post title",
                        "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
                        "origin": "http://whereitcamefrom.com/posts/zzzzz",
                        "description": "friends_post description",
                        "contentType": "text/plain",
                        "content": "friends_post content",
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
                        "visibility": "FRIENDS",
                        "visibleTo": [],
                        "unlisted": False
                        }
        self.create_mock_post(friends_post, self.authorProfile)

        private_post = {"title": "private_post title",
                        "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
                        "origin": "http://whereitcamefrom.com/posts/zzzzz",
                        "description": "private_post description",
                        "contentType": "text/plain",
                        "content": "private_post content",
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
                        "visibility": "PRIVATE",
                        "visibleTo": [],
                        "unlisted": False
                        }
        self.create_mock_post(private_post, self.authorProfile)

        server_only_post = {"title": "server_only_post title",
                            "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
                            "origin": "http://whereitcamefrom.com/posts/zzzzz",
                            "description": "server_only_post description",
                            "contentType": "text/plain",
                            "content": "server_only_post content",
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
                            "visibility": "SERVERONLY",
                            "visibleTo": [],
                            "unlisted": False
                            }
        self.create_mock_post(server_only_post, self.authorProfile)

        expected_output = [public_post, public_post_2]
        expected_author = [self.authorProfile, self.authorProfile2]
        self.client.login(username=self.username, password=self.password)
        response = self.client.get("/api/posts/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        for i in range(len(expected_output)):
            self.assert_post(response.data[i], expected_output[i], expected_author[i])
