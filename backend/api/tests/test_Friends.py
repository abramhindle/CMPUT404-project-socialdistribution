import uuid

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import RequestsClient

from .util import get_author_id
from ..models import Follow, AuthorProfile
import json


class FriendsTestCase(TestCase):
    client = RequestsClient()
    username = "test123"
    password = "pw123"

    username2 = "test123_2"
    password2 = "pw123_2"

    username3 = "test123_3"
    password3 = "pw123_3"

    def setUp(self):
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user2 = User.objects.create_user(username=self.username2, password=self.password2)
        self.user3 = User.objects.create_user(username=self.username3, password=self.password3)

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

        self.user_id = get_author_id(self.authorProfile.host, self.authorProfile.id, False)
        self.user_id2 = get_author_id(self.authorProfile2.host, self.authorProfile2.id, False)
        self.user_id3 = get_author_id(self.authorProfile3.host, self.authorProfile3.id, False)

        # author is the author sending the request
        # friend is the author who you want to follow/friend
        self.input_params = {
            "query": "friendrequest",
            "author": {
                "id": self.user_id,
                "host": self.authorProfile2.host,
                "displayName": self.authorProfile.displayName,
                "url": self.user_id,
            },
            "friend": {
                "id": self.user_id2,
                "host": self.authorProfile2.host,
                "displayName": self.authorProfile2.displayName,
                "url": self.user_id2,
            }
        }

        self.unfollow_input_params = {
            "query": "unfollow",
            "author": {
                "id": self.user_id,
                "host": self.authorProfile2.host,
                "displayName": self.authorProfile.displayName,
                "url": self.user_id,
            },
            "friend": {
                "id": self.user_id2,
                "host": self.authorProfile2.host,
                "displayName": self.authorProfile2.displayName,
                "url": self.user_id2,
            }
        }

    def test_invalid_auth(self):
        # test if the endpoint is protected by auth
        response = self.client.post("/api/friendrequest")
        self.assertEqual(response.status_code, 403)

    def test_missing_arguments(self):
        self.client.login(username=self.username, password=self.password)
        for key in self.input_params.keys():
            invalid_input = self.input_params.copy()
            invalid_input.pop(key)
            response = self.client.post("/api/friendrequest", data=invalid_input, content_type="application/json")
            self.assertEqual(response.status_code, 400)

        for key in ["author", "friend"]:
            invalid_input = self.input_params.copy()
            invalid_input[key].pop("id")
            response = self.client.post("/api/friendrequest", data=invalid_input, content_type="application/json")
            self.assertEqual(response.status_code, 400)

    def test_invalid_methods(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get("/api/friendrequest/")
        self.assertEqual(response.status_code, 405)
        response = self.client.put("/api/friendrequest/")
        self.assertEqual(response.status_code, 405)
        response = self.client.delete("/api/friendrequest/")
        self.assertEqual(response.status_code, 405)
        self.client.logout()

    def test_follow_local(self):
        Follow.objects.all().delete()
        self.client.login(username=self.username, password=self.password)
        response = self.client.post("/api/friendrequest", data=self.input_params, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), "Friend Request Success")

        row = Follow.objects.all()[0]
        self.assertEqual(row.authorA, self.input_params["author"]["id"])
        self.assertEqual(row.authorB, self.input_params["friend"]["id"])
        self.assertEqual(row.status, "FOLLOWING")

    # this is scenario where authorA already follows authorB,
    # then either authorB sends authorA a follow request ("accept the friend request")
    def test_friend_local(self):
        Follow.objects.all().delete()
        self.client.login(username=self.username, password=self.password)

        Follow.objects.create(authorA=self.input_params["friend"]["id"],
                              authorB=self.input_params["author"]["id"],
                              status="FOLLOWING")

        response = self.client.post("/api/friendrequest", data=self.input_params, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), "Friend Request Success")

        results = Follow.objects.all()

        self.assertEqual(results[0].authorA, self.input_params["friend"]["id"])
        self.assertEqual(results[0].authorB, self.input_params["author"]["id"])
        self.assertEqual(results[0].status, "FRIENDS")

        self.assertEqual(results[1].authorA, self.input_params["author"]["id"])
        self.assertEqual(results[1].authorB, self.input_params["friend"]["id"])
        self.assertEqual(results[1].status, "FRIENDS")

    # send follow request but content in author is not your own
    def test_follow_wrong_author(self):
        Follow.objects.all().delete()
        self.client.login(username=self.username3, password=self.password3)

        response = self.client.post("/api/unfriend", data=self.unfollow_input_params,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), "Unfollow Request Fail")

    # send unfollow request but content in author is not your own
    def test_unfollow_wrong_author(self):
        Follow.objects.all().delete()
        self.client.login(username=self.username3, password=self.password3)

        response = self.client.post("/api/unfriend", data=self.unfollow_input_params, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), "Unfollow Request Fail")

    def test_unfriend_local_success(self):
        Follow.objects.all().delete()
        self.client.login(username=self.username, password=self.password)
        Follow.objects.create(authorA=self.unfollow_input_params["friend"]["id"],
                              authorB=self.unfollow_input_params["author"]["id"],
                              status="FRIENDS")

        Follow.objects.create(authorA=self.unfollow_input_params["author"]["id"],
                              authorB=self.unfollow_input_params["friend"]["id"],
                              status="FRIENDS")

        response = self.client.post("/api/unfriend", data=self.unfollow_input_params, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), "Unfriend Request Success")

        results = Follow.objects.all()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].authorA, self.input_params["friend"]["id"])
        self.assertEqual(results[0].authorB, self.input_params["author"]["id"])
        self.assertEqual(results[0].status, "FOLLOWING")

    def test_unfollow_local_success(self):
        Follow.objects.all().delete()
        self.client.login(username=self.username, password=self.password)
        Follow.objects.create(authorA=self.unfollow_input_params["author"]["id"],
                              authorB=self.unfollow_input_params["friend"]["id"],
                              status="FOLLOWING")

        response = self.client.post("/api/unfriend", data=self.unfollow_input_params, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), "Unfollow Request Success")

        results = Follow.objects.all()
        self.assertEqual(len(results), 0)

    def test_follow_non_existing_user(self):
        Follow.objects.all().delete()
        self.client.login(username=self.username, password=self.password)
        invalid_input = self.input_params.copy()
        invalid_input["friend"]["id"] = invalid_input["friend"]["host"] + str(uuid.uuid4())
        response = self.client.post("/api/unfriend", data=invalid_input, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), "Unfollow Request Fail")

    def test_unfollow_non_existing_user(self):
        Follow.objects.all().delete()
        self.client.login(username=self.username, password=self.password)
        invalid_input = self.unfollow_input_params.copy()
        invalid_input["friend"]["id"] = invalid_input["friend"]["host"] + str(uuid.uuid4())
        response = self.client.post("/api/unfriend", data=invalid_input, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), "Unfollow Request Fail")
