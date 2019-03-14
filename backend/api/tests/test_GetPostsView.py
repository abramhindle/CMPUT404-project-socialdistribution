from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client, RequestFactory
from rest_framework.test import RequestsClient
from ..models import Post, AuthorProfile, Follow, Category
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

        self.user_id_1_escaped = get_author_id(self.authorProfile1.host, self.authorProfile1.id, True)
        self.user_id_2_escaped = get_author_id(self.authorProfile2.host, self.authorProfile2.id, True)
        self.user_id_3_escaped = get_author_id(self.authorProfile3.host, self.authorProfile3.id, True)
        self.user_id_4_escaped = get_author_id(self.authorProfile4.host, self.authorProfile4.id, True)
        self.user_id_5_escaped = get_author_id(self.authorProfile5.host, self.authorProfile5.id, True)


        Category.objects.create(name="test_category_1")
        Category.objects.create(name="test_category_2")

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
            "author": {
                "id": "http://127.0.0.1:5454/author/{}".format(self.authorProfile1.id),
                "host": "http://127.0.0.1:5454/",
                "displayName": self.authorProfile1.displayName,
                "url": "http://127.0.0.1:5454/author/{}".format(self.authorProfile1.id),
                "github": self.authorProfile1.github
            },
            "categories": ["test_category_1", "test_category_2"],
            "published": "2015-03-09T13:07:04+00:00",
            "id": "de305d54-75b4-431b-adb2-eb6b9e546013",
            "visibility": "PUBLIC",
            "visibleTo": [],
            "unlisted": False
                    }

        self.private_post = {
            "title": "private_post title",
            "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
            "origin": "http://whereitcamefrom.com/posts/zzzzz",
            "description": "private_post description",
            "contentType": "text/plain",
            "content": "private_post content",
            "author": {
                "id": "http://127.0.0.1:5454/author/{}".format(self.authorProfile1.id),
                "host": "http://127.0.0.1:5454/",
                "displayName": self.authorProfile1.displayName,
                "url": "http://127.0.0.1:5454/author/{}".format(self.authorProfile1.id),
                "github": self.authorProfile1.github
            },
            "categories": ["test_category_1", "test_category_2"],
            "published": "2015-03-09T13:07:04+00:00",
            "id": "de305d54-75b4-431b-adb2-eb6b9e546013",
            "visibility": "PRIVATE",
            "visibleTo": [],
            "unlisted": False
            }

        self.foaf_post = {
                "title": "foaf_post title",
                 "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
                 "origin": "http://whereitcamefrom.com/posts/zzzzz",
                 "description": "foaf_post description",
                 "contentType": "text/plain",
                 "content": "foaf_post content",
                 "author": {
                     "id": "http://127.0.0.1:5454/author/".format(self.authorProfile1.id),
                     "host": "http://127.0.0.1:5454/",
                     "displayName": self.authorProfile1.displayName,
                     "url": "http://127.0.0.1:5454/author/".format(self.authorProfile1.id),
                     "github": self.authorProfile1.github
                 },
                 "categories": ["test_category_1", "test_category_2"],
                 "published": "2015-03-09T13:07:04+00:00",
                 "id": "de305d54-75b4-431b-adb2-eb6b9e546013",
                 "visibility": "FOAF",
                 "visibleTo": [],
                 "unlisted": False
                 }

        self.friends_post = {
                "title": "friends_post title",
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

        self.server_only_post = {
                "title": "server_only_post title",
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

    def test_get_public_posts(self):
        Post.objects.all().delete()
        self.client.login(username=self.username2, password=self.password2)
        create_mock_post(self.public_post1, self.authorProfile1)
        create_mock_post(self.public_post2, self.authorProfile1)

        response = self.client.get("/api/author/{}/posts".format(self.authorProfile1.id))
        created_posts = Post.objects.all()

        expected_output = {
            "query": "posts",
            "count": 2,
            "posts": [self.public_post2, self.public_post1]
        }

        expected_author_list = [self.authorProfile1] * expected_output["count"] 

        assert_post_response(response, expected_output, expected_author_list)
        self.client.logout()

    def test_get_posts_with_invalid_author_id(self):
        Post.objects.all().delete()
        self.client.login(username=self.username1, password=self.password1)
        fake_uuid = uuid.uuid4()

        response = self.client.get("/api/author/{}/posts".format(fake_uuid))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), "Error: Author does not exist!")
        self.client.logout()

    # This test checks if author 2 can retrieve all posts of author 1 if it is visible to author 2
    def test_get_own_foaf_post(self):
        Post.objects.all().delete()
        Follow.objects.all().delete()

        create_mock_post(self.public_post1, self.authorProfile1)
        create_mock_post(self.public_post2, self.authorProfile1)
        create_mock_post(self.foaf_post, self.authorProfile1)

        self.client.login(username=self.username1, password=self.password1)

        response = self.client.get("/api/author/{}/posts".format(self.authorProfile1.id))
        created_posts = Post.objects.all()
        expected_output = {
            "query": "posts",
            "count": 3,
            "posts": [self.foaf_post, self.public_post2, self.public_post1]
        }

        expected_author_list = [self.authorProfile1] * expected_output["count"]
        assert_post_response(response, expected_output, expected_author_list)
        self.client.logout()

    def test_get_foaf_post_is_foaf(self):
        # make sure there's no post existing
        Post.objects.all().delete()
        Follow.objects.all().delete()

        create_mock_post(self.public_post1, self.authorProfile1)
        create_mock_post(self.public_post2, self.authorProfile1)
        create_mock_post(self.foaf_post, self.authorProfile1)

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

        response = self.client.get("/api/author/{}/posts".format(self.authorProfile1.id))

        expected_output = {
            "query": "posts",
            "count": 3,
            "posts": [self.foaf_post, self.public_post2, self.public_post1]
        }
        expected_author_list = [self.authorProfile1] * expected_output["count"]

        assert_post_response(response, expected_output, expected_author_list)
        self.client.logout()

    def test_get_foaf_post_is_not_foaf(self):
        # make sure there's no post existing
        Post.objects.all().delete()
        Follow.objects.all().delete()

        create_mock_post(self.public_post1, self.authorProfile1)
        create_mock_post(self.public_post2, self.authorProfile1)
        create_mock_post(self.foaf_post, self.authorProfile1)

        self.client.login(username=self.username5, password=self.password5)

        response = self.client.get("/api/author/{}/posts".format(self.authorProfile1.id))
        created_posts = Post.objects.all()

        expected_output = {
            "query": "posts",
            "count": 2,
            "posts": [self.public_post2, self.public_post1]
        }
        expected_author_list = [self.authorProfile1] * expected_output["count"]

        assert_post_response(response, expected_output, expected_author_list)
        self.client.logout()

    def test_get_own_friends_post(self):
        Post.objects.all().delete()
        Follow.objects.all().delete()

        create_mock_post(self.public_post1, self.authorProfile1)
        create_mock_post(self.public_post2, self.authorProfile1)
        create_mock_post(self.friends_post, self.authorProfile1)

        self.client.login(username=self.username1, password=self.password1)

        response = self.client.get("/api/author/{}/posts".format(self.authorProfile1.id))
        created_posts = Post.objects.all()
        expected_output = {
            "query": "posts",
            "count": 3,
            "posts": [self.friends_post, self.public_post2, self.public_post1]
        }

        expected_author_list = [self.authorProfile1] * expected_output["count"] 
        assert_post_response(response, expected_output, expected_author_list)
        self.client.logout()

    def test_get_friend_post_is_friend(self):
        Post.objects.all().delete()
        Follow.objects.all().delete()

        create_mock_post(self.public_post1, self.authorProfile1)
        create_mock_post(self.public_post2, self.authorProfile1)
        create_mock_post(self.friends_post, self.authorProfile1)

        Follow.objects.create(authorA=self.user_id_1,
                              authorB=self.user_id_2,
                              status="FRIENDS")

        Follow.objects.create(authorA=self.user_id_2,
                              authorB=self.user_id_1,
                              status="FRIENDS")

        self.client.login(username=self.username2, password=self.password2)

        response = self.client.get("/api/author/{}/posts".format(self.authorProfile1.id))
        created_posts = Post.objects.all()

        expected_output = {
            "query": "posts",
            "count": 3,
            "posts": [self.friends_post, self.public_post2, self.public_post1]
        }
        expected_author_list = [self.authorProfile1] * expected_output["count"]

        assert_post_response(response, expected_output, expected_author_list)
        self.client.logout()

    def test_get_friend_post_is_not_friend(self):
        Post.objects.all().delete()
        Follow.objects.all().delete()

        create_mock_post(self.public_post1, self.authorProfile1)
        create_mock_post(self.public_post2, self.authorProfile1) 
        create_mock_post(self.friends_post, self.authorProfile1)

        self.client.login(username=self.username2, password=self.password2)

        response = self.client.get("/api/author/{}/posts".format(self.authorProfile1.id))
        created_posts = Post.objects.all()

        expected_output = {
            "query": "posts",
            "count": 2,
            "posts": [self.public_post2, self.public_post1]
        }
        expected_author_list = [self.authorProfile1] * expected_output["count"]

        assert_post_response(response, expected_output, expected_author_list)
        self.client.logout()

    def test_get_own_private_post(self):
        Post.objects.all().delete()

        create_mock_post(self.public_post1, self.authorProfile1)
        create_mock_post(self.public_post2, self.authorProfile1) 
        create_mock_post(self.private_post, self.authorProfile1) 
        self.client.login(username=self.username1, password=self.password1)

        response = self.client.get("/api/author/{}/posts".format(self.authorProfile1.id))
        created_posts = Post.objects.all()
        expected_output = {
            "query": "posts",
            "count": 3,
            "posts": [self.private_post, self.public_post2, self.public_post1]
        }

        expected_author_list = [self.authorProfile1] * expected_output["count"] 
        assert_post_response(response, expected_output, expected_author_list)
        self.client.logout()

    # this test attempts to see if a user can access another user's private post
    def test_get_private_post(self):
        Post.objects.all().delete()

        create_mock_post(self.public_post1, self.authorProfile1)
        create_mock_post(self.public_post2, self.authorProfile1) 
        create_mock_post(self.private_post, self.authorProfile1) 
        self.client.login(username=self.username2, password=self.password2)

        response = self.client.get("/api/author/{}/posts".format(self.authorProfile1.id))

        expected_output = {
            "query": "posts",
            "count": 2,
            "posts": [self.public_post2, self.public_post1]
        }
        # This test asserts that author2 can get public posts of author 1 but not the private
        # Currently there are 3 posts in the DB
        expected_author_list = [self.authorProfile1] * expected_output["count"] 
        assert_post_response(response, expected_output, expected_author_list)
        self.client.logout()
