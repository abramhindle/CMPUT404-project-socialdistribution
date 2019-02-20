from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import RequestsClient
from ..models import Follow
import json

class AuthorProfileCase(TestCase):
    client = RequestsClient()
    username = "test123"
    password = "pw123"

    def setUp(self):
        self.user = User.objects.create_user(username=self.username, password=self.password)
        # self.authorProfile = AuthorProfile.objects.create(host="http://127.0.0.1:5454/",
        #                                                   displayName="Lara Croft",
        #                                                   github="http://github.com/laracroft",
        #                                                   user=self.user)

    def test_invalid_auth(self):
        # test if the endpoint is protected by auth
        response = self.client.post("/api/friendrequest")
        self.assertEqual(response.status_code, 403)

    def test_missing_arguments(self):
        input_params = {
            "query": "friendrequest",
            "author": {
                "id": "http://127.0.0.1:5454/author/de305d54-75b4-431b-adb2-eb6b9e546013",
                "host": "http://127.0.0.1:5454/",
                "displayName": "Greg Johnson",
                "url": "http://127.0.0.1:5454/author/de305d54-75b4-431b-adb2-eb6b9e546013",
            },
            "friend": {
                "id": "http://127.0.0.1:5454/author/de305d54-75b4-431b-adb2-eb6b9e637281",
                "host": "http://127.0.0.1:5454/",
                "displayName": "Lara Croft",
                "url": "http://127.0.0.1:5454/author/de305d54-75b4-431b-adb2-eb6b9e546013",

            }
        }
        self.client.login(username=self.username, password=self.password)
        for key in input_params.keys():
            invalid_input = input_params.copy()
            invalid_input.pop(key)
            response = self.client.post("/api/friendrequest", data=invalid_input, content_type="application/json")
            self.assertEqual(response.status_code, 400)

        for outer_key in ["author", "friend"]:
            for inner_key in input_params[outer_key]:
                invalid_input = input_params.copy()
                invalid_input[outer_key].pop(inner_key)
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

    def test_follow(self):
        Follow.objects.all().delete()
        self.client.login(username=self.username, password=self.password)
        input_params = {
            "query":"friendrequest",
            "author": {
                "id":"http://127.0.0.1:5454/author/de305d54-75b4-431b-adb2-eb6b9e546013",
                "host":"http://127.0.0.1:5454/",
                "displayName":"Greg Johnson",
                        "url":"http://127.0.0.1:5454/author/de305d54-75b4-431b-adb2-eb6b9e546013",
            },
            "friend": {
                "id":"http://127.0.0.1:5454/author/de305d54-75b4-431b-adb2-eb6b9e637281",
                "host":"http://127.0.0.1:5454/",
                "displayName":"Lara Croft",
                "url":"http://127.0.0.1:5454/author/de305d54-75b4-431b-adb2-eb6b9e546013",

            }
        }
        response = self.client.post("/api/friendrequest", data=input_params, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), "Friend Request Success")

        row = Follow.objects.all()[0]
        self.assertEqual(row.authorA, input_params["author"]["id"])
        self.assertEqual(row.authorB, input_params["friend"]["id"])
        self.assertEqual(row.status, "FOLLOWING")

    def test_friend(self):
        Follow.objects.all().delete()
        self.client.login(username=self.username, password=self.password)
        input_params = {
            "query": "friendrequest",
            "author": {
                "id": "http://127.0.0.1:5454/author/de305d54-75b4-431b-adb2-eb6b9e546013",
                "host": "http://127.0.0.1:5454/",
                "displayName": "Greg Johnson",
                "url": "http://127.0.0.1:5454/author/de305d54-75b4-431b-adb2-eb6b9e546013",
            },
            "friend": {
                "id": "http://127.0.0.1:5454/author/de305d54-75b4-431b-adb2-eb6b9e637281",
                "host": "http://127.0.0.1:5454/",
                "displayName": "Lara Croft",
                "url": "http://127.0.0.1:5454/author/de305d54-75b4-431b-adb2-eb6b9e546013",

            }
        }
        Follow.objects.create(authorA=input_params["friend"]["id"],
                              authorB=input_params["author"]["id"],
                              status="FOLLOWING")

        response = self.client.post("/api/friendrequest", data=input_params, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), "Friend Request Success")

        results = Follow.objects.all()
        self.assertEqual(results[0].authorA, input_params["friend"]["id"])
        self.assertEqual(results[0].authorB, input_params["author"]["id"])
        self.assertEqual(results[0].status, "FRIENDS")

        self.assertEqual(results[0].authorA, input_params["author"]["id"])
        self.assertEqual(results[0].authorB, input_params["friend"]["id"])
        self.assertEqual(results[0].status, "FRIENDS")
