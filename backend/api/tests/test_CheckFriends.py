import urllib
from uuid import uuid4

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import RequestsClient
from ..models import Follow, AuthorProfile
from .util import *
import json


class CheckFollowersTestCase(TestCase):
    client = RequestsClient()
    username = "test123"
    password = "pw123"

    username2 = "test123_2"
    password2 = "pw123_2"

    username3 = "test123_3"
    password3 = "pw123_3"

    username4 = "test123_4"
    password4 = "pw123_4"

    def setUp(self):
        # create user
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user2 = User.objects.create_user(username=self.username2, password=self.password2)
        self.user3 = User.objects.create_user(username=self.username3, password=self.password3)
        self.user4 = User.objects.create_user(username=self.username4, password=self.password4)

        self.authorProfile = AuthorProfile.objects.create(host="http://127.0.0.1:5454/",
                                                          displayName="Lara Croft",
                                                          github="http://github.com/laracroft",
                                                          user=self.user)

        self.authorProfile2 = AuthorProfile.objects.create(host="http://127.0.0.1:5454/",
                                                           displayName="Lara Croft number 2",
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

        self.user_id = get_author_id(self.authorProfile.host, self.authorProfile.id, False)
        self.user_id2 = get_author_id(self.authorProfile2.host, self.authorProfile2.id, False)
        self.user_id3 = get_author_id(self.authorProfile3.host, self.authorProfile3.id, False)
        self.user_id4 = get_author_id(self.authorProfile4.host, self.authorProfile4.id, False)

        Follow.objects.create(authorA=self.user_id,
                              authorB=self.user_id2,
                              status="FRIENDS")

        Follow.objects.create(authorA=self.user_id,
                              authorB=self.user_id3,
                              status="FOLLOWING")

        Follow.objects.create(authorA=self.user_id,
                              authorB=self.user_id4,
                              status="FRIENDS")

    def test_invalid_methods(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.put("/api/author/{}/friends/".format(self.authorProfile.id))
        self.assertEqual(response.status_code, 405)
        response = self.client.delete("/api/author/{}/friends/".format(self.authorProfile.id))
        self.assertEqual(response.status_code, 405)
        self.client.logout()

    def test_get_author_friends_list_with_no_auth(self):
        response = self.client.get("/api/author/{}/friends/".format(self.authorProfile.id))
        self.assertEqual(response.status_code, 403)

    def test_get_author_friends_list_with_no_author_id(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get("/api/author/{}/friends/".format(""))
        self.assertEqual(response.status_code, 400)
        self.client.logout()

    def test_get_author_friends_list_with_non_existing_author_id(self):
        self.client.login(username=self.username, password=self.password)
        fake_id = str(uuid4())
        response = self.client.get("/api/author/{}/friends/".format(fake_id))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), "Error: Author Does Not Exist")
        self.client.logout()

    # should get a list of <authorid>'s friends
    def test_get_author_friends_list_with_auth(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get("/api/author/{}/friends/".format(self.authorProfile.id))
        self.assertEqual(response.status_code, 200)

        expected_output = {
            "query": "friends",
            "authors": [
                self.user_id2,
                self.user_id4
            ]
        }
        self.assertEqual(expected_output["query"], response.data["query"])
        self.assertTrue(len(expected_output["authors"]), len(response.data["authors"]))
        for ele in expected_output["authors"]:
            self.assertTrue(ele in response.data["authors"])
        self.client.logout()


    def test_get_author_friends_list_with_auth_post(self):
        self.client.login(username=self.username, password=self.password)

        payload = {
            "query": "friends",
            "author": "<authorid>",
            "authors": [self.user_id3, self.user_id4]
        }

        response = self.client.post("/api/author/{}/friends/".format(self.authorProfile.id), data=payload)
        self.assertEqual(response.status_code, 200)

        expected_output = {
            "query": "friends",
            "author": self.user_id,
            "authors": [self.user_id4]
        }
        self.assertEqual(expected_output["query"], response.data["query"])
        self.assertTrue(len(expected_output["authors"]), len(response.data["authors"]))

        for ele in expected_output["authors"]:
            self.assertTrue(ele in response.data["authors"])
        self.client.logout()
