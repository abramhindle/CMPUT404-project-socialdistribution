from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import RequestsClient
from ..models import Category, Post, AuthorProfile, Follow
from ..serializers import PostSerializer
import json
import uuid
from .util import *
from django.conf import settings


class PostTestCase(TestCase):
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

    input_params = {"title": "A post title about a post about web dev",
                    "description": "This post discusses stuff -- brief",
                    "contentType": "text/plain",
                    "content": "Some content",
                    "categories": ["test_category_1", "test_category_2"],
                    "visibility": "PUBLIC",
                    "visibleTo": [],
                    "unlisted": False,
                    }

    public_post_1 = {"title": "A post title about a post about web dev",
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
        self.user1 = User.objects.create_user(username=self.username1, password=self.password1)
        self.user2 = User.objects.create_user(username=self.username2, password=self.password2)
        self.user3 = User.objects.create_user(username=self.username3, password=self.password3)
        self.user4 = User.objects.create_user(username=self.username4, password=self.password4)
        self.user5 = User.objects.create_user(username=self.username5, password=self.password5)

        self.authorProfile1 = AuthorProfile.objects.create(host=settings.BACKEND_URL,
                                                           displayName="Lara Croft",
                                                           github="http://github.com/laracroft",
                                                           user=self.user1)

        self.authorProfile2 = AuthorProfile.objects.create(host=settings.BACKEND_URL,
                                                           displayName="Lara Croft2",
                                                           github="http://github.com/laracroft2",
                                                           user=self.user2)

        self.authorProfile3 = AuthorProfile.objects.create(host=settings.BACKEND_URL,
                                                           displayName="Lara Croft number 3",
                                                           github="http://github.com/laracroft3",
                                                           user=self.user3)

        self.authorProfile4 = AuthorProfile.objects.create(host=settings.BACKEND_URL,
                                                           displayName="Lara Croft number 4",
                                                           github="http://github.com/laracroft4",
                                                           user=self.user4)

        self.authorProfile5 = AuthorProfile.objects.create(host=settings.BACKEND_URL,
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

    def test_invalid_auth(self):
        # test if the endpoint is protected by auth
        response = self.client.post("/api/posts/", data=self.input_params, content_type="application/json")
        self.assertEqual(response.status_code, 403)

    def test_create_post_fail(self):
        self.client.login(username=self.username1, password=self.password1)

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
        self.client.login(username=self.username1, password=self.password1)

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
        assert_post(created_post, expected_post, self.authorProfile1)
        self.assertEqual(json.loads(response.content), "Create Post Success")

        # test valid input with non-existing categories
        input_params = self.input_params.copy()
        expected_post["categories"] = ["non_existing_category"]
        input_params["categories"] = ["non_existing_category"]
        response = self.client.post("/api/posts/", data=input_params, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        created_post = Post.objects.all()[1]
        created_post = PostSerializer(created_post).data
        assert_post(created_post, expected_post, self.authorProfile1)
        self.assertEqual(json.loads(response.content), "Create Post Success")
        self.client.logout()

    def test_create_post_with_visible_to_success(self):
        Post.objects.all().delete()
        self.client.login(username=self.username1, password=self.password1)
        test_input = self.private_post.copy()
        test_input["visibleTo"] = ["{}author/{}".format(self.authorProfile2.host, str(self.authorProfile2.id))]
        response = self.client.post("/api/posts/", data=test_input, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        created_post = Post.objects.all()[0]
        created_post = PostSerializer(created_post).data
        assert_post(created_post, test_input, self.authorProfile1)
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

        self.client.login(username=self.username1, password=self.password1)
        response = self.client.put("/api/posts", data=json.dumps(self.input_params), content_type="application/json")

        self.assertEqual(response.status_code, 200)

        created_post = Post.objects.all()[0]
        created_post = PostSerializer(created_post).data

        assert_post(created_post, expected_post, self.authorProfile1)
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

        self.client.login(username=self.username1, password=self.password1)  # make the posts first
        self.client.put("/api/posts", data=json.dumps(self.input_params), content_type="application/json")

        post_id = Post.objects.all()[0].id
        put_update_post_response = self.client.put("/api/posts/{}".format(post_id), data=json.dumps(updated_post),
                                                   content_type="application/json")
        self.assertEqual(put_update_post_response.status_code, 200)

        updated_post = Post.objects.all()[0]
        updated_post = PostSerializer(updated_post).data

        assert_post(updated_post, expected_post, self.authorProfile1)

    # adding visibleTo when post is not private
    def test_create_post_with_visible_to_fail(self):
        for current_input in [self.public_post_1, self.friends_post, self.foaf_post, self.server_only_post]:
            Post.objects.all().delete()
            self.client.login(username=self.username1, password=self.password1)
            test_input = current_input.copy()
            test_input["visibleTo"] = ["{}author/{}".format(self.authorProfile2.host, str(self.authorProfile2.id))]
            response = self.client.post("/api/posts/", data=test_input, content_type="application/json")
            self.assertEqual(response.status_code, 400)
            self.assertEqual(json.loads(response.content), "Error: Post must be private if visibleTo is provided")
            self.client.logout()

    # adding visibleTo for non existing user
    def test_create_post_with_visible_to_non_existing_user(self):
        Post.objects.all().delete()
        self.client.login(username=self.username1, password=self.password1)
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
        self.client.login(username=self.username1, password=self.password1)

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

        create_mock_post(self.public_post_1, self.authorProfile1)
        create_mock_post(self.public_post_2, self.authorProfile2)
        create_mock_post(self.foaf_post, self.authorProfile1)
        create_mock_post(self.friends_post, self.authorProfile1)
        create_mock_post(self.private_post, self.authorProfile1)
        create_mock_post(self.server_only_post, self.authorProfile1)

        expected_output = {
            "query": "posts",
            "count": 2,
            "posts": [self.public_post_1, self.public_post_2]
        }
        expected_author = [self.authorProfile1, self.authorProfile2]
        response = self.client.get("/api/posts/")
        assert_post_response(response, expected_output, expected_author)
        self.client.logout()

    def test_delete_post_no_post_id(self):
        Post.objects.all().delete()
        self.client.login(username=self.username1, password=self.password1)
        response = self.client.delete("/api/posts/")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), "Error: Post ID is Missing")

    def test_delete_post_non_existing_post_id(self):
        Post.objects.all().delete()
        self.client.login(username=self.username1, password=self.password1)
        non_existing_post_id = uuid.uuid4()
        response = self.client.delete("/api/posts/{}".format(non_existing_post_id))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), "Error: Post Does Not Exist")

    # try to delete someone's post
    def test_delete_post_invalid_author(self):
        Post.objects.all().delete()
        self.client.login(username=self.username1, password=self.password1)
        mock_post = create_mock_post(self.public_post_2, self.authorProfile2)
        response = self.client.delete("/api/posts/{}".format(mock_post.id))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), "Error: Invalid Author")

    def test_delete_post_success(self):
        Post.objects.all().delete()
        self.client.login(username=self.username1, password=self.password1)
        mock_post = create_mock_post(self.public_post_1, self.authorProfile1)
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

        self.client.login(username=self.username1, password=self.password1)
        post_id = Post.objects.all()[0].id

        put_update_post_response = self.client.put("/api/posts/{}".format(post_id), data=json.dumps(updated_post),
                                                   content_type="application/json")

        self.assertEqual(put_update_post_response.status_code, 400)
        self.client.logout()

    ######################### tests for getting posts with post id #####################

    def test_get_public_posts_with_post_id(self):
        Post.objects.all().delete()
        self.client.login(username=self.username2, password=self.password2)

        create_mock_post(self.public_post_1, self.authorProfile1)
        create_mock_post(self.public_post_2, self.authorProfile1)
        test_post_obj = create_mock_post(self.public_post_1, self.authorProfile1)

        response = self.client.get("/api/posts/{}".format(test_post_obj.id))

        expected_output = {
            "query": "posts",
            "count": 1,
            "posts": [self.public_post_1]
        }

        expected_author_list = [self.authorProfile1] * expected_output["count"]

        assert_post_response(response, expected_output, expected_author_list)
        self.client.logout()

    def test_get_posts_with_invalid_post_id(self):
        Post.objects.all().delete()
        self.client.login(username=self.username1, password=self.password1)
        fake_uuid = uuid.uuid4()

        response = self.client.get("/api/posts/{}".format(fake_uuid))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), "Error: Post does not exist!")
        self.client.logout()

    # This test checks if author 2 can retrieve all posts of author 1 if it is visible to author 2
    def test_get_own_foaf_post_with_post_id(self):
        Post.objects.all().delete()
        Follow.objects.all().delete()

        create_mock_post(self.public_post_1, self.authorProfile1)
        create_mock_post(self.public_post_2, self.authorProfile1)
        test_post_obj = create_mock_post(self.foaf_post, self.authorProfile1)

        self.client.login(username=self.username1, password=self.password1)

        response = self.client.get("/api/posts/{}".format(test_post_obj.id))

        expected_output = {
            "query": "posts",
            "count": 1,
            "posts": [self.foaf_post]
        }

        expected_author_list = [self.authorProfile1] * expected_output["count"]
        assert_post_response(response, expected_output, expected_author_list)
        self.client.logout()

    def test_get_foaf_post_is_foaf_with_post_id(self):
        # make sure there's no post existing
        Post.objects.all().delete()
        Follow.objects.all().delete()

        create_mock_post(self.public_post_1, self.authorProfile1)
        create_mock_post(self.public_post_2, self.authorProfile1)
        test_post_obj = create_mock_post(self.foaf_post, self.authorProfile1)

        Follow.objects.create(authorA=self.user_id_1,
                              authorB=self.user_id_2,
                              status="FRIENDS")

        Follow.objects.create(authorA=self.user_id_2,
                              authorB=self.user_id_1,
                              status="FRIENDS")

        Follow.objects.create(authorA=self.user_id_1,
                              authorB=self.user_id_3,
                              status="FRIENDS")

        Follow.objects.create(authorA=self.user_id_3,
                              authorB=self.user_id_1,
                              status="FRIENDS")

        Follow.objects.create(authorA=self.user_id_3,
                              authorB=self.user_id_4,
                              status="FRIENDS")

        Follow.objects.create(authorA=self.user_id_4,
                              authorB=self.user_id_3,
                              status="FRIENDS")

        Follow.objects.create(authorA=self.user_id_3,
                              authorB=self.user_id_5,
                              status="FRIENDS")

        Follow.objects.create(authorA=self.user_id_5,
                              authorB=self.user_id_3,
                              status="FRIENDS")

        self.client.login(username=self.username5, password=self.password5)

        response = self.client.get("/api/posts/{}".format(test_post_obj.id))

        expected_output = {
            "query": "posts",
            "count": 1,
            "posts": [self.foaf_post]
        }
        expected_author_list = [self.authorProfile1] * expected_output["count"]

        assert_post_response(response, expected_output, expected_author_list)
        self.client.logout()

    def test_get_foaf_post_is_not_foaf_with_post_id(self):
        # make sure there's no post existing
        Post.objects.all().delete()
        Follow.objects.all().delete()

        create_mock_post(self.public_post_1, self.authorProfile1)
        create_mock_post(self.public_post_2, self.authorProfile1)
        test_post_obj = create_mock_post(self.foaf_post, self.authorProfile1)

        self.client.login(username=self.username5, password=self.password5)

        response = self.client.get("/api/posts/{}".format(test_post_obj.id))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), "Error: You do not have permission to view this post")
        self.client.logout()

    def test_get_own_friends_post_with_post_id(self):
        Post.objects.all().delete()
        Follow.objects.all().delete()

        create_mock_post(self.public_post_1, self.authorProfile1)
        create_mock_post(self.public_post_2, self.authorProfile1)
        test_post_obj = create_mock_post(self.friends_post, self.authorProfile1)

        self.client.login(username=self.username1, password=self.password1)

        response = self.client.get("/api/posts/{}".format(test_post_obj.id))

        expected_output = {
            "query": "posts",
            "count": 1,
            "posts": [self.friends_post]
        }

        expected_author_list = [self.authorProfile1] * expected_output["count"]
        assert_post_response(response, expected_output, expected_author_list)
        self.client.logout()

    def test_get_friend_post_is_friend_with_post_id(self):
        Post.objects.all().delete()
        Follow.objects.all().delete()

        create_mock_post(self.public_post_1, self.authorProfile1)
        create_mock_post(self.public_post_2, self.authorProfile1)
        test_post_obj = create_mock_post(self.friends_post, self.authorProfile1)

        Follow.objects.create(authorA=self.user_id_1,
                              authorB=self.user_id_2,
                              status="FRIENDS")

        Follow.objects.create(authorA=self.user_id_2,
                              authorB=self.user_id_1,
                              status="FRIENDS")

        self.client.login(username=self.username2, password=self.password2)

        response = self.client.get("/api/posts/{}".format(test_post_obj.id))

        expected_output = {
            "query": "posts",
            "count": 1,
            "posts": [self.friends_post]
        }
        expected_author_list = [self.authorProfile1] * expected_output["count"]

        assert_post_response(response, expected_output, expected_author_list)
        self.client.logout()

    def test_get_friend_post_is_not_friend_with_post_id(self):
        Post.objects.all().delete()
        Follow.objects.all().delete()

        create_mock_post(self.public_post_1, self.authorProfile1)
        create_mock_post(self.public_post_2, self.authorProfile1)
        test_post_obj = create_mock_post(self.friends_post, self.authorProfile1)

        self.client.login(username=self.username2, password=self.password2)

        response = self.client.get("/api/posts/{}".format(test_post_obj.id))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), "Error: You do not have permission to view this post")
        self.client.logout()

    def test_get_own_private_post_with_post_id(self):
        Post.objects.all().delete()

        create_mock_post(self.public_post_1, self.authorProfile1)
        create_mock_post(self.public_post_2, self.authorProfile1)
        test_post_obj = create_mock_post(self.private_post, self.authorProfile1)
        self.client.login(username=self.username1, password=self.password1)

        response = self.client.get("/api/posts/{}".format(test_post_obj.id))

        expected_output = {
            "query": "posts",
            "count": 1,
            "posts": [self.private_post]
        }

        expected_author_list = [self.authorProfile1] * expected_output["count"]
        assert_post_response(response, expected_output, expected_author_list)
        self.client.logout()

    # this test attempts to see if a user can access another user's private post
    def test_get_private_post_with_post_id(self):
        Post.objects.all().delete()

        create_mock_post(self.public_post_1, self.authorProfile1)
        create_mock_post(self.public_post_2, self.authorProfile1)
        test_post_obj = create_mock_post(self.private_post, self.authorProfile1)
        self.client.login(username=self.username2, password=self.password2)

        response = self.client.get("/api/posts/{}".format(test_post_obj.id))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), "Error: You do not have permission to view this post")
        self.client.logout()

    def test_get_server_only_post_with_post_id(self):
        Post.objects.all().delete()

        create_mock_post(self.public_post_1, self.authorProfile1)
        create_mock_post(self.public_post_2, self.authorProfile1)
        test_post_obj = create_mock_post(self.server_only_post, self.authorProfile1)
        self.client.login(username=self.username1, password=self.password1)

        response = self.client.get("/api/posts/{}".format(test_post_obj.id))

        expected_output = {
            "query": "posts",
            "count": 1,
            "posts": [self.server_only_post]
        }

        expected_author_list = [self.authorProfile1] * expected_output["count"]
        assert_post_response(response, expected_output, expected_author_list)
        self.client.logout()
