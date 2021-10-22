import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from http import HTTPStatus

from backend.models import Author


class AuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_authors = 5
        User.objects.bulk_create([
            User(username="AuthorListViewTest_{}".format(idx),
            password=make_password("Margret Thatcher"),
            is_active=True
            ) for idx in range(number_of_authors)
        ])
        for author_id in range(number_of_authors):
            Author.objects.create(
                user=User.objects.get(username="AuthorListViewTest_{}".format(author_id)),
                display_name="Test unit{}".format(author_id),
            )

    def test_view_url_exists_at_desired_location(self):
        res = self.client.get("/authors/")
        self.assertEqual(res.status_code, 200)

    def test_correct_number_of_authors(self):
        res = self.client.get("/authors/")
        self.assertEqual(res.status_code, 200)
        body = json.loads(res.content.decode("utf-8"))
        self.assertEqual(len(body["items"]), 5)

class AuthorViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        uuid_list = [
            "95a1e643-180c-4de6-8fc5-9cb48a216fbe",
            "856c692d-2514-4d06-80fc-4c4312188db3",
            "bf453da8-459c-4064-a6bc-21d8f24c6d7f",
            "4d5baaf2-0cc5-4fd0-89a7-21ddc46e6e2e",
            "b3c492b6-a690-4b89-b2c1-23d21433fdce",
        ]
        number_of_authors = len(uuid_list)
        User.objects.bulk_create([
            User(username="AuthorViewTest_{}".format(idx),
            password=make_password("Margret Thatcher"),
            is_active=True
            ) for idx in range(number_of_authors)
        ])
        for author_id in range(number_of_authors):
            Author.objects.create(
                id=uuid_list[author_id],
                user=User.objects.get(username="AuthorViewTest_{}".format(author_id)),
                display_name="Test unit{}".format(author_id),
            )
    def test_author_not_found(self):
        res = self.client.get("/author/282848/")
        self.assertEqual(res.status_code, 404)

    def test_valid_author(self):
        res = self.client.get("/author/b3c492b6-a690-4b89-b2c1-23d21433fdce/")
        self.assertEqual(res.status_code, 200)

class SignupViewTest(TestCase):
    def test_get(self):
        res = self.client.get("/signup/")

        self.assertEqual(res.status_code, HTTPStatus.OK)

    def test_post(self):
        data = {
            'username':'test',
            'display_name': 'test',
            'password1': 'margaret thatcher',
            'password2': 'margaret thatcher',
        }
        res = self.client.post("/signup/", data = data)
        self.assertRedirects(res, "/admin-approval/", fetch_redirect_response=False)

class LoginViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        uuid_list = [
            "95a1e643-180c-4de6-8fc5-9cb48a216fbe",
            "856c692d-2514-4d06-80fc-4c4312188db3",
            "bf453da8-459c-4064-a6bc-21d8f24c6d7f",
        ]
        number_of_authors = len(uuid_list)
        User.objects.bulk_create([
            User(username="LoginViewTest{}".format(idx),
            password=make_password("Margret Thatcher"),
            is_active = False if idx == 2 else True
            ) for idx in range(number_of_authors)
        ])
        for author_id in range(number_of_authors):
            Author.objects.create(
                id=uuid_list[author_id],
                user=User.objects.get(username="LoginViewTest{}".format(author_id)),
                display_name="Test unit{}".format(author_id),
                url="http://127.0.0.1:8000/author/{}".format(uuid_list[author_id]),
                host="http://127.0.0.1:8000/",
            )
    def test_get(self):
        res = self.client.get("/login/")

        self.assertEqual(res.status_code, HTTPStatus.OK)

    def test_valid_login(self):
        data = {
            "username": "LoginViewTest0",
            "password":"Margret Thatcher"
        }
        res = self.client.post("/login/", data=data, follow=True)
        self.assertTrue(res.context['user'].is_authenticated)
    
    def test_invalid_login(self):
        data = {
            "username": "asdf",
            "password":"asdf"
        }
        res = self.client.post("/login/", data=data, follow=True)
        self.assertFalse(res.context['user'].is_authenticated)

    def test_non_active_login(self):
        data = {
            "username": "LoginViewTest2",
            "password":"Margret Thatcher"
        }
        res = self.client.post("/login/", data=data, follow=True)
        self.assertFalse(res.context['user'].is_authenticated)
        self.assertFalse(res.context['user'].is_active)
