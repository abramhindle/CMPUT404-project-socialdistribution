import json
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

TEST_USERNAME = 'bob'
TEST_PASSWORD = 'password'


class AuthorTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        get_user_model().objects.create_user(username=TEST_USERNAME, password=TEST_PASSWORD)

    def test_authors(self):
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        res = self.client.get('/api/v1/authors/')
        self.assertEqual(res.status_code, 200)
        body = json.loads(res.content.decode('utf-8'))
        self.assertEqual(body['type'], 'authors')
        self.assertEqual(len(body['items']), 1)

    def test_authors_require_login(self):
        res = self.client.get('/api/v1/authors/')
        self.assertEqual(res.status_code, 403)

    def test_create_author(self):
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        res = self.client.post('/api/v1/authors/', {'username': 'alice', 'password': 'some_password'})
        self.assertEqual(res.status_code, 405)

    def test_allow_api_users(self):
        api_user_username = 'api_user'
        api_user = get_user_model().objects.create_user(username=api_user_username, password=TEST_PASSWORD)
        api_user.is_api_user = True
        api_user.save()

        self.client.login(username=api_user_username, password=TEST_PASSWORD)
        res = self.client.get('/api/v1/authors/')
        self.assertEqual(res.status_code, 200)
