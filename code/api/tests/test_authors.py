# python manage.py test api

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer
import json

from socialDistribution.models import Author

# Documentation and code samples taken from the following references:
# Django Software Foundation, https://docs.djangoproject.com/en/3.2/intro/tutorial05/
# Django Software Foundation, https://docs.djangoproject.com/en/3.2/topics/testing/overview/
# Python Software Foundation, https://docs.python.org/3/library/unittest.html

def create_author(id, username, displayName, githubUrl):
    user = mixer.blend(User, username=username)
    return Author.objects.create(id=id, username=username, displayName=displayName, githubUrl=githubUrl, user=user)


class AuthorsViewTests(TestCase):

    def test_get_authors_basic(self):
        expected = json.dumps({"type": "authors", "items": []})
        response = self.client.get(reverse("api:authors"))

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, expected)

    def test_get_authors_single(self):
        author = create_author(
            1,
            "user1",
            "John Doe",
            "https://github.com/johndoe"
        )
        expected = {
            "type": "author",
            "id": "http://127.0.0.1:8000/api/author/1",
            "host": "http://127.0.0.1:8000/api/",
            "displayName": "John Doe",
            "url": "http://127.0.0.1:8000/api/author/1",
            "github": "https://github.com/johndoe",
            "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
        }

        response = self.client.get(reverse("api:authors"))
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get("type"), "authors")
        self.assertEqual(len(data.get("items")), 1)

        author = data.get("items")[0]
        self.assertDictEqual(author, expected)

    def test_get_authors_multiple(self):
        user = mixer.blend(User)
        author1 = create_author(
            1,
            "user1",
            "John Smith",
            "https://github.com/smith"
        )
        author2 = create_author(
            2,
            "user2",
            "Apple J Doe",
            "https://github.com/apple"
        )
        author3 = create_author(
            3,
            "user3",
            "Jane Smith G. Sr.",
            "https://github.com/another"
        )

        expected = [
            {
                "type": "author",
                "id": "http://127.0.0.1:8000/api/author/1",
                "host": "http://127.0.0.1:8000/api/",
                "displayName": "John Smith",
                "url": "http://127.0.0.1:8000/api/author/1",
                "github": "https://github.com/smith",
                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
            },
            {
                "type": "author",
                "id": "http://127.0.0.1:8000/api/author/2",
                "host": "http://127.0.0.1:8000/api/",
                "displayName": "Apple J Doe",
                "url": "http://127.0.0.1:8000/api/author/2",
                "github": "https://github.com/apple",
                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
            },
            {
                "type": "author",
                "id": "http://127.0.0.1:8000/api/author/3",
                "host": "http://127.0.0.1:8000/api/",
                "displayName": "Jane Smith G. Sr.",
                "url": "http://127.0.0.1:8000/api/author/3",
                "github": "https://github.com/another",
                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
            }
        ]

        response = self.client.get(reverse("api:authors"))
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get("type"), "authors")
        self.assertEqual(len(data.get("items")), 3,
                         "Expected to recieve list of 3 authors")

        items = data.get("items")
        self.assertListEqual(items, expected)

    def test_get_author(self):
        author = create_author(
            1,
            "user1",
            "John Doe",
            "https://github.com/johndoe"
        )
        expected = {
            "type": "author",
            "id": "http://127.0.0.1:8000/api/author/1",
            "host": "http://127.0.0.1:8000/api/",
            "displayName": "John Doe",
            "url": "http://127.0.0.1:8000/api/author/1",
            "github": "https://github.com/johndoe",
            "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
        }
        response = self.client.get(
            reverse("api:author", kwargs={"author_id": 1}))

        actual = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(actual, expected)
