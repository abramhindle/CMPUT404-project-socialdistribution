from django.test import TestCase
import json
from django.urls import reverse
from django.contrib.auth.models import User
from http import HTTPStatus

from backend.models import Author


class AuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_authors = 5

        for author_id in range(number_of_authors):
            user = User.objects.create_user(username="testuser-{}".format(author_id))
            Author.objects.create(
                user=user,
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
        number_of_authors = 5
        uuid_list = [
            "95a1e643-180c-4de6-8fc5-9cb48a216fbe",
            "856c692d-2514-4d06-80fc-4c4312188db3",
            "bf453da8-459c-4064-a6bc-21d8f24c6d7f",
            "4d5baaf2-0cc5-4fd0-89a7-21ddc46e6e2e",
            "b3c492b6-a690-4b89-b2c1-23d21433fdce",
        ]
        for author_id in range(number_of_authors):
            user = User.objects.create_user(username="testuser-{}".format(author_id))
            Author.objects.create(
                id=uuid_list[author_id],
                user=user,
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
        
        self.assertEqual(res.status_code, HTTPStatus.OK)