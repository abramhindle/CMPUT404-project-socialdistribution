from django.test import TestCase
from rest_framework.test import APIClient

client = APIClient() # the mock http client

class AuthTestCase(TestCase):
    def test_register_simple_happy(self):
        payload = {
            'username': 'test_register_simple_happy',
            'password': ';askdjfxzc0-v8923k5jm0-Z*xklcasxcKLjKj()*^$!^',
        }
        res = client.post('/register/', payload, format='json')
        '''
        expected sample response
        {
            "displayName": "LUcasdf",
            "github": "https://github.com/asdf",
            "host": "http://127.0.0.1:8000/register/",
            "id": "http://127.0.0.1:8000/author/8d2718f8-a957-418c-b826-f51bbb34f57f/",
            "type": "author",
            "url": "http://127.0.0.1:8000/author/8d2718f8-a957-418c-b826-f51bbb34f57f/"
        }
        '''
        assert res.data['author']['displayName'] == payload['username']
        assert res.data['author']['id'] == res.data['author']['url'] and res.data['author']['id'].startswith('http')
        assert res.data['author']['type'] == 'author'
        assert res.status_code == 200

    def test_register_full_happy(self):
        payload = {
            'username': 'test_register_full_happy',
            'password': ';askdjfxzc0-v8923k5jm0-Z*xklcasxcKLjKj()*^$!^',
            "display_name": "Lucas_Z",
            "github_url": "https://github.com/asdf",
        }
        res = client.post('/register/', payload, format='json')
        '''
        expected sample response
        {
            "displayName": "Lucas_Z",
            "github": "https://github.com/asdf",
            "host": "http://127.0.0.1:8000/register/",
            "id": "http://127.0.0.1:8000/author/8d2718f8-a957-418c-b826-f51bbb34f57f/",
            "type": "author",
            "url": "http://127.0.0.1:8000/author/8d2718f8-a957-418c-b826-f51bbb34f57f/"
        }
        '''
        assert res.data['author']['displayName'] == payload['display_name']
        assert res.data['author']['id'] == res.data['author']['url'] and res.data['author']['id'].startswith('http')
        assert res.data['author']['type'] == 'author'

        assert res.data['author']['github'] == payload['github_url']
        assert res.status_code == 200

