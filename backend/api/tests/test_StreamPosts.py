from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client, RequestFactory
from rest_framework.test import RequestsClient
from ..models import Post, AuthorProfile, Follow, Category
from ..serializers import PostSerializer
import json
import uuid
from .util import *
from django.conf import settings

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
    host = settings.BACKEND_URL

    def setUp(self):
        self.user1 = User.objects.create_user(username=self.username1, password=self.password1)
        self.user2 = User.objects.create_user(username=self.username2, password=self.password2)
        self.user3 = User.objects.create_user(username=self.username3, password=self.password3)
        self.user4 = User.objects.create_user(username=self.username4, password=self.password4)
        self.user5 = User.objects.create_user(username=self.username5, password=self.password5)

        self.authorProfile1 = AuthorProfile.objects.create(host=self.host,
                                                          displayName="Lara Croft",
                                                          github="http://github.com/laracroft",
                                                          user=self.user1)

        self.authorProfile2 = AuthorProfile.objects.create(
                                                            host=self.host,
                                                            displayName="Lara Croft2",
                                                            github="http://github.com/laracroft2",
                                                            user=self.user2)

        self.authorProfile3 = AuthorProfile.objects.create(host=self.host,
                                                           displayName="Lara Croft number 3",
                                                           github="http://github.com/laracroft3",
                                                           user=self.user3)

        self.authorProfile4 = AuthorProfile.objects.create(host=self.host,
                                                           displayName="Lara Croft number 4",
                                                           github="http://github.com/laracroft4",
                                                           user=self.user4)

        self.authorProfile5 = AuthorProfile.objects.create(host=self.host,
                                                           displayName="Lara Croft number 5",
                                                           github="http://github.com/laracroft5",
                                                           user=self.user5)

        self.user_id_1 = get_author_id(self.authorProfile1.host, self.authorProfile1.id, False)
        self.user_id_2 = get_author_id(self.authorProfile2.host, self.authorProfile2.id, False)
        self.user_id_3 = get_author_id(self.authorProfile3.host, self.authorProfile3.id, False)
        self.user_id_4 = get_author_id(self.authorProfile4.host, self.authorProfile4.id, False)
        self.user_id_5 = get_author_id(self.authorProfile5.host, self.authorProfile5.id, False)

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

        self.friends_post = {
                "title": "friends_post title",
                "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
                "origin": "http://whereitcamefrom.com/posts/zzzzz",
                "description": "friends_post description",
                "contentType": "text/plain",
                "content": "friends_post content",
                "categories": ["test_category_1", "test_category_2"],
                "published": "2015-03-09T13:07:04+00:00",
                "id": "de305d54-75b4-431b-adb2-eb6b9e546016",
                "visibility": "FRIENDS",
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
                "categories": ["test_category_1", "test_category_2"],
                "published": "2015-03-09T13:07:04+00:00",
                "id": "de305d54-75b4-431b-adb2-eb6b9e546013",
                "visibility": "PRIVATE",
                "visibleTo": [],
                "unlisted": False
                }

        self.visible_to_post = {
                "title": "private post visible to author 1",
                "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
                "origin": "http://whereitcamefrom.com/posts/zzzzz",
                "description": "private_post description",
                "contentType": "text/plain",
                "content": "private_post content",
                "categories": ["test_category_1", "test_category_2"],
                "published": "2015-03-09T13:07:04+00:00",
                "id": "de305d54-75b4-431b-adb2-eb6b9e546013",
                "visibility": "PRIVATE",
                "visibleTo": ["{}author/{}".format(self.authorProfile1.host, str(self.authorProfile1.id))],
                "unlisted": False
                }

        self.server_only_post = {
                "title": "server_only_post title",
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

    def test_invalid_auth(self):
        response = self.client.get("/api/author/posts")
        self.assertEqual(response.status_code, 403)


    def test_get_own_posts_in_stream(self):
        Post.objects.all().delete()
        Follow.objects.all().delete()
        self.client.login(username=self.username1, password=self.password1)

        create_mock_post(self.public_post1, self.authorProfile1)
        create_mock_post(self.public_post2, self.authorProfile1)

        response = self.client.get("/api/author/posts")

        expected_output = {
            "query": "posts",
            "count": 2,
            "posts": [self.public_post2, self.public_post1]
        }

        expected_author_list = [self.authorProfile1, self.authorProfile1] 

        self.assertEqual(response.status_code, 200)
        assert_post_response(response, expected_output, expected_author_list)
        self.client.logout()

    def test_get_public_post_following_others(self):
        Post.objects.all().delete()
        Follow.objects.all().delete()
        self.client.login(username=self.username1, password=self.password1)

        Follow.objects.create(
                authorA=self.user_id_1,
                authorB=self.user_id_2,
                status="FOLLOWING")
        
        create_mock_post(self.public_post1, self.authorProfile1)
        create_mock_post(self.public_post2, self.authorProfile2)
        create_mock_post(self.public_post2, self.authorProfile2)

        response = self.client.get("/api/author/posts")

        expected_output = {
            "query": "posts",
            "count": 3,
            "posts": [self.public_post2, self.public_post2, self.public_post1]
        }

        expected_author_list = [self.authorProfile2, self.authorProfile2, self.authorProfile1] 

        self.assertEqual(response.status_code, 200)
        assert_post_response(response, expected_output, expected_author_list)
        self.client.logout()

    
    def test_get_unlisted_post(self):
        Post.objects.all().delete()
        Follow.objects.all().delete()
        self.client.login(username=self.username1, password=self.password1)

        Follow.objects.create(
                authorA=self.user_id_1,
                authorB=self.user_id_3,
                status="FOLLOWING")

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
        self.client.logout()

    def test_get_friends_post_in_stream(self):
        Post.objects.all().delete()
        Follow.objects.all().delete()
        self.client.login(username=self.username1, password=self.password1)

        Follow.objects.create(authorA=self.user_id_1,
                              authorB=self.user_id_2,
                              status="FRIENDS")

        Follow.objects.create(authorA=self.user_id_2,
                              authorB=self.user_id_1,
                              status="FRIENDS")

        create_mock_post(self.public_post1, self.authorProfile1)
        create_mock_post(self.public_post2, self.authorProfile2)
        create_mock_post(self.friends_post, self.authorProfile2)

        response = self.client.get("/api/author/posts")

        expected_output = {
            "query": "posts",
            "count": 3,
            "posts": [self.friends_post, self.public_post2, self.public_post1]
        }

        expected_author_list = [self.authorProfile2, self.authorProfile2, self.authorProfile1] 

        self.assertEqual(response.status_code, 200)
        assert_post_response(response, expected_output, expected_author_list)
        self.client.logout()

    def test_stream_posts_but_not_friend(self):
        Follow.objects.all().delete()
        Post.objects.all().delete()
        self.client.login(username=self.username3, password=self.password3)

        Follow.objects.create(authorA=self.user_id_1,
                              authorB=self.user_id_2,
                              status="FRIENDS")

        Follow.objects.create(authorA=self.user_id_2,
                              authorB=self.user_id_1,
                              status="FRIENDS")

        create_mock_post(self.public_post1, self.authorProfile3)
        create_mock_post(self.public_post2, self.authorProfile3)
        create_mock_post(self.friends_post, self.authorProfile2)

        response = self.client.get("/api/author/posts")

        expected_output = {
            "query": "posts",
            "count": 2,
            "posts": [self.public_post2, self.public_post1]
        }

        expected_author_list = [self.authorProfile3, self.authorProfile3] 

        self.assertEqual(response.status_code, 200)
        assert_post_response(response, expected_output, expected_author_list)
        self.client.logout()

    def test_private_posts_not_in_stream(self):
        Follow.objects.all().delete()
        Post.objects.all().delete()
        self.client.login(username=self.username1, password=self.password1)

        create_mock_post(self.public_post1, self.authorProfile1)
        create_mock_post(self.public_post2, self.authorProfile1)
        create_mock_post(self.private_post, self.authorProfile2)

        response = self.client.get("/api/author/posts")

        expected_output = {
            "query": "posts",
            "count": 2,
            "posts": [self.public_post2, self.public_post1]
        }

        expected_author_list = [self.authorProfile1, self.authorProfile1] 

        self.assertEqual(response.status_code, 200)
        assert_post_response(response, expected_output, expected_author_list)
        self.client.logout()

    def test_private_posts_visible_to_in_stream(self):
        Follow.objects.all().delete()
        Post.objects.all().delete()

        self.client.login(username=self.username1, password=self.password1)

        Follow.objects.create(authorA=self.user_id_1,
                        authorB=self.user_id_2,
                        status="FRIENDS")

        create_mock_post(self.public_post1, self.authorProfile1)
        create_mock_post(self.public_post2, self.authorProfile2)
        create_mock_post(self.visible_to_post, self.authorProfile2)

        response = self.client.get("/api/author/posts")

        expected_output = {
            "query": "posts",
            "count": 3,
            "posts": [self.visible_to_post, self.public_post2, self.public_post1]
        }

        expected_author_list = [self.authorProfile2, self.authorProfile2, self.authorProfile1] 

        self.assertEqual(response.status_code, 200)
        assert_post_response(response, expected_output, expected_author_list)
        self.client.logout()

    def test_get_private_but_not_visible_to(self):
        Follow.objects.all().delete()
        Post.objects.all().delete()

        self.client.login(username=self.username2, password=self.password2)

        Follow.objects.create(authorA=self.user_id_2,
                authorB=self.user_id_3,
                status="FRIENDS")

        create_mock_post(self.public_post1, self.authorProfile3)
        create_mock_post(self.public_post2, self.authorProfile3)
        create_mock_post(self.visible_to_post, self.authorProfile3)

        response = self.client.get("/api/author/posts")
        expected_output = {
            "query": "posts",
            "count": 2,
            "posts": [self.public_post2, self.public_post1]
        }

        expected_author_list = [ self.authorProfile3, self.authorProfile3] 

        self.assertEqual(response.status_code, 200)
        assert_post_response(response, expected_output, expected_author_list)
        self.client.logout()


    def test_get_stream_server_only(self):
        Follow.objects.all().delete()
        Post.objects.all().delete()
        self.client.login(username=self.username1, password=self.password1)

        Follow.objects.create(
                authorA=self.user_id_1,
                authorB=self.user_id_3,
                status="FRIENDS")

        Follow.objects.create(
                authorA=self.user_id_1,
                authorB=self.user_id_2,
                status="FRIENDS")
        
        create_mock_post(self.public_post1, self.authorProfile1)
        create_mock_post(self.public_post2, self.authorProfile2)
        create_mock_post(self.server_only_post, self.authorProfile3)

        response = self.client.get("/api/author/posts")

        expected_output = {
            "query": "posts",
            "count": 3,
            "posts": [self.server_only_post, self.public_post2, self.public_post1]
        }

        expected_author_list = [self.authorProfile3, self.authorProfile2, self.authorProfile1] 

        self.assertEqual(response.status_code, 200)
        assert_post_response(response, expected_output, expected_author_list)
        self.client.logout()
