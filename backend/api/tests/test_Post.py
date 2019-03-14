from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client, RequestFactory
from rest_framework.test import RequestsClient
from ..models import Category, Post, AuthorProfile
from ..serializers import PostSerializer
import json
import uuid
from .util import *


class PostTestCase(TestCase):
    client = RequestsClient()
    username = "test123"
    password = "pw123"

    username2 = "test123_2"
    password2 = "pw123_2"
    input_params = {"title": "A post title about a post about web dev",
                    "description": "This post discusses stuff -- brief",
                    "contentType": "text/plain",
                    "content": "Some content",
                    "categories": ["test_category_1", "test_category_2"],
                    "visibility": "PUBLIC",
                    "visibleTo": [],
                    "unlisted": False,
                    }

    public_post = {"title": "A post title about a post about web dev",
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

    # Second public post made by author 2
    public_post_2 = {"title": "public_post_2 title",
                     "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
                     "origin": "http://whereitcamefrom.com/posts/zzzzz",
                     "description": "public_post_2 description",
                     "contentType": "text/plain",
                     "content": "public_post_2 content",
                     "categories": ["test_category_1", "test_category_2"],
                     "published": "2015-03-09T13:07:04+00:00",
                     "id": "de305d54-75b4-431b-adb2-eb6b9e546013",
                     "visibility": "PUBLIC",
                     "visibleTo": [],
                     "unlisted": False
                     }

    foaf_post = {"title": "foaf_post title",
                 "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
                 "origin": "http://whereitcamefrom.com/posts/zzzzz",
                 "description": "foaf_post description",
                 "contentType": "text/plain",
                 "content": "foaf_post content",
                 "categories": ["test_category_1", "test_category_2"],
                 "published": "2015-03-09T13:07:04+00:00",
                 "id": "de305d54-75b4-431b-adb2-eb6b9e546013",
                 "visibility": "FOAF",
                 "visibleTo": [],
                 "unlisted": False
                 }

    friends_post = {"title": "friends_post title",
                    "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
                    "origin": "http://whereitcamefrom.com/posts/zzzzz",
                    "description": "friends_post description",
                    "contentType": "text/plain",
                    "content": "friends_post content",
                    "categories": ["test_category_1", "test_category_2"],
                    "published": "2015-03-09T13:07:04+00:00",
                    "id": "de305d54-75b4-431b-adb2-eb6b9e546013",
                    "visibility": "FRIENDS",
                    "visibleTo": [],
                    "unlisted": False
                    }

    private_post = {"title": "private_post title",
                    "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
                    "origin": "http://whereitcamefrom.com/posts/zzzzz",
                    "description": "private_post description",
                    "contentType": "text/plain",
                    "content": "private_post content",
                    "categories": ["test_category_1", "test_category_2"],
                    "published": "2015-03-09T13:07:04+00:00",
                    "id": "de305d54-75b4-431b-adb2-eb6b9e546013",
                    "visibility": "PRIVATE",
                    "visibleTo": [],
                    "unlisted": False
                    }

    server_only_post = {"title": "server_only_post title",
                        "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
                        "origin": "http://whereitcamefrom.com/posts/zzzzz",
                        "description": "server_only_post description",
                        "contentType": "text/plain",
                        "content": "server_only_post content",
                        "categories": ["test_category_1", "test_category_2"],
                        "published": "2015-03-09T13:07:04+00:00",
                        "id": "de305d54-75b4-431b-adb2-eb6b9e546013",
                        "visibility": "SERVERONLY",
                        "visibleTo": [],
                        "unlisted": False
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
        response = self.client.post("/api/posts/", data=self.input_params, content_type="application/json")
        self.assertEqual(response.status_code, 403)

    def test_create_post_fail(self):
        self.client.login(username=self.username, password=self.password)

        for key in self.input_params.keys():
            if (key == "unlisted" or key == "visibleTo"):
                continue
            invalid_input = self.input_params.copy()
            # test fields is empty
            invalid_input[key] = ""
            if (key == "categories"):
                invalid_input[key] = []
            response = self.client.post("/api/posts/", data=invalid_input, content_type="application/json")
            self.assertEqual(response.status_code, 400)

            # test field is missing
            invalid_input.pop(key)
            response = self.client.post("/api/posts/", data=invalid_input, content_type="application/json")
            self.assertEqual(response.status_code, 400)

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
                         "categories": ["test_category_1", "test_category_2"],
                         "published": "2015-03-09T13:07:04+00:00",
                         "id": "de305d54-75b4-431b-adb2-eb6b9e546013",
                         "visibility": "PUBLIC",
                         "visibleTo": [],
                         "unlisted": False
                         }

        # test valid input with existing categories
        response = self.client.post("/api/posts/", data=self.input_params, content_type="application/json")

        created_post = Post.objects.all()[0]
        created_post = PostSerializer(created_post).data
        self.assertEqual(response.status_code, 200)
        assert_post(created_post, expected_post, self.authorProfile)
        self.assertEqual(json.loads(response.content), "Create Post Success")

        # test valid input with non-existing categories
        input_params = self.input_params.copy()
        expected_post["categories"] = ["non_existing_category"]
        input_params["categories"] = ["non_existing_category"]
        response = self.client.post("/api/posts/", data=input_params, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        created_post = Post.objects.all()[1]
        created_post = PostSerializer(created_post).data
        assert_post(created_post, expected_post, self.authorProfile)
        self.assertEqual(json.loads(response.content), "Create Post Success")
        self.client.logout()

    def test_create_post_with_visible_to_success(self):
        Post.objects.all().delete()
        self.client.login(username=self.username, password=self.password)
        test_input = self.private_post.copy()
        test_input["visibleTo"] = ["{}author/{}".format(self.authorProfile2.host, str(self.authorProfile2.id))]
        response = self.client.post("/api/posts/", data=test_input, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        created_post = Post.objects.all()[0]
        created_post = PostSerializer(created_post).data
        assert_post(created_post, test_input, self.authorProfile)
        self.assertEqual(json.loads(response.content), "Create Post Success")
        self.client.logout()

    def test_put_post(self):
        Post.objects.all().delete()

        expected_post = {
            "title": "A post title about a post about web dev",
            "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
            "origin": "http://whereitcamefrom.com/posts/zzzzz",
            "description": "This post discusses stuff -- brief",
            "contentType": "text/plain",
            "content": "Some content",
            "categories": ["test_category_1", "test_category_2"],
            "published": "2015-03-09T13:07:04+00:00",
            "id": "de305d54-75b4-431b-adb2-eb6b9e546013",
            "visibility": "PUBLIC",
            "visibleTo": [],
            "unlisted": False
        }

        self.client.login(username=self.username, password=self.password)
        response = self.client.put("/api/posts", data=json.dumps(self.input_params), content_type="application/json")

        self.assertEqual(response.status_code, 200)

        created_post = Post.objects.all()[0]
        created_post = PostSerializer(created_post).data

        assert_post(created_post, expected_post, self.authorProfile)
        self.assertEqual(json.loads(response.content), "Create Post Success")

    def test_put_update_post(self):
        Post.objects.all().delete()

        expected_post = {
            "title": "I update this title to show the power of TDD",
            "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
            "origin": "http://whereitcamefrom.com/posts/zzzzz",
            "description": "this post is the power of TDD and updating through PUT",
            "contentType": "text/plain",
            "content": "Some content 2",
            "categories": ["test_category_1", "test_category_2", "test_category_3"],
            "published": "2015-03-09T13:07:04+00:00",
            "id": "de305d54-75b4-431b-adb2-eb6b9e546013",
            "visibility": "PRIVATE",
            "visibleTo": ["http://localhost.com:8000/{}".format(self.authorProfile2.id)],
            "unlisted": True
        }

        
        updated_post = {
            "title": "I update this title to show the power of TDD",
            "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
            "description": "this post is the power of TDD and updating through PUT",
            "contentType": "text/plain",
            "content": "Some content 2",
            "categories": ["test_category_1", "test_category_2", "test_category_3"],
            "visibility": "PRIVATE",
            "visibleTo": ["http://localhost.com:8000/{}".format(self.authorProfile2.id)],
            "unlisted": True
        }

        self.client.login(username=self.username, password=self.password)  # make the posts first
        self.client.put("/api/posts", data=json.dumps(self.input_params), content_type="application/json")

        post_id = Post.objects.all()[0].id
        put_update_post_response = self.client.put("/api/posts/{}".format(post_id), data=json.dumps(updated_post),
                                                   content_type="application/json")
        self.assertEqual(put_update_post_response.status_code, 200)

        updated_post = Post.objects.all()[0]
        updated_post = PostSerializer(updated_post).data

        assert_post(updated_post, expected_post, self.authorProfile)

    # adding visibleTo when post is not private
    def test_create_post_with_visible_to_fail(self):
        for current_input in [self.public_post, self.friends_post, self.foaf_post, self.server_only_post]:
            Post.objects.all().delete()
            self.client.login(username=self.username, password=self.password)
            test_input = current_input.copy()
            test_input["visibleTo"] = ["{}author/{}".format(self.authorProfile2.host, str(self.authorProfile2.id))]
            response = self.client.post("/api/posts/", data=test_input, content_type="application/json")
            self.assertEqual(response.status_code, 400)
            self.assertEqual(json.loads(response.content), "Error: Post must be private if visibleTo is provided")
            self.client.logout()

    # adding visibleTo for non existing user
    def test_create_post_with_visible_to_non_existing_user(self):
        Post.objects.all().delete()
        self.client.login(username=self.username, password=self.password)
        test_input = self.private_post.copy()
        test_input["visibleTo"] = ["{}author/{}".format(self.authorProfile2.host, str(uuid.uuid4()))]
        response = self.client.post("/api/posts/", data=test_input, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), "Error: User in visibleTo does not exist")
        self.client.logout()

    # this should return all public posts
    def test_get_post_without_id(self):
        # make sure there's no post existing
        Post.objects.all().delete()
        self.client.login(username=self.username, password=self.password)

        # test no public posts
        response = self.client.get("/api/posts/")
        self.assertEqual(response.status_code, 200)
        expected_output = {
            "query": "posts",
            "count": 0,
            "posts": []
        }
        self.assertEqual(response.data["query"], expected_output["query"])
        self.assertEqual(response.data["count"], expected_output["count"])
        self.assertEqual(len(response.data["posts"]), 0)

        create_mock_post(self.public_post, self.authorProfile)
        create_mock_post(self.public_post_2, self.authorProfile2)
        create_mock_post(self.foaf_post, self.authorProfile)
        create_mock_post(self.friends_post, self.authorProfile)
        create_mock_post(self.private_post, self.authorProfile)
        create_mock_post(self.server_only_post, self.authorProfile)

        expected_output = {
            "query": "posts",
            "count": 2,
            "posts": [self.public_post, self.public_post_2]
        }
        expected_author = [self.authorProfile, self.authorProfile2]
        response = self.client.get("/api/posts/")
        assert_post_response(response, expected_output, expected_author)
        self.client.logout()

    def test_delete_post_no_post_id(self):
        Post.objects.all().delete()
        self.client.login(username=self.username, password=self.password)
        response = self.client.delete("/api/posts/")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), "Error: Post ID is Missing")

    def test_delete_post_non_existing_post_id(self):
        Post.objects.all().delete()
        self.client.login(username=self.username, password=self.password)
        non_existing_post_id = uuid.uuid4()
        response = self.client.delete("/api/posts/{}".format(non_existing_post_id))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), "Error: Post Does Not Exist")

    # try to delete someone's post
    def test_delete_post_invalid_author(self):
        Post.objects.all().delete()
        self.client.login(username=self.username, password=self.password)
        mock_post = create_mock_post(self.public_post_2, self.authorProfile2)
        response = self.client.delete("/api/posts/{}".format(mock_post.id))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), "Error: Invalid Author")

    def test_delete_post_success(self):
        Post.objects.all().delete()
        self.client.login(username=self.username, password=self.password)
        mock_post = create_mock_post(self.public_post, self.authorProfile)
        self.assertEqual(len(Post.objects.all()), 1)
        response = self.client.delete("/api/posts/{}".format(mock_post.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), "Delete Post Success")
        self.assertEqual(len(Post.objects.all()), 0)

    def test_put_update_wrong_user_post(self):
        Post.objects.all().delete()
        self.client.login(username=self.username2, password=self.password2)
        self.client.put("/api/posts", data=json.dumps(self.public_post_2), content_type="application/json")
        self.client.logout()

        updated_post = {
            "title": "I update this title to show the power of TDD",
            "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
            "description": "this post is the power of TDD and updating through PUT",
            "contentType": "text/plain",
            "content": "Some content 2",
            "categories": ["test_category_1", "test_category_2", "test_category_3"],
            "unlisted": True
        }

        self.client.login(username=self.username, password=self.password)
        post_id = Post.objects.all()[0].id

        put_update_post_response = self.client.put("/api/posts/{}".format(post_id), data=json.dumps(updated_post),
                                                   content_type="application/json")

        self.assertEqual(put_update_post_response.status_code, 400)
        self.client.logout()
