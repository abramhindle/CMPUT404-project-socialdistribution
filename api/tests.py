import json
from django.test import TestCase, Client
from django.contrib.auth import get_user_model


class AuthorTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        get_user_model().objects.create_user(username='bob', password='password')

    def test_authors(self):
        self.client.login(username='bob', password='password')
        res = self.client.get('/api/v1/authors/')
        self.assertEqual(res.status_code, 200)
        body = json.loads(res.content.decode('utf-8'))
        self.assertEqual(body['type'], 'authors')
        self.assertEqual(len(body['items']), 1)

    def test_authors_require_login(self):
        res = self.client.get('/api/v1/authors/')
        self.assertEqual(res.status_code, 403)

    def test_create_author(self):
        self.client.login(username='bob', password='password')
        res = self.client.post('/api/v1/authors/', {'username': 'alice', 'password': 'password'})
        self.assertEqual(res.status_code, 405)
