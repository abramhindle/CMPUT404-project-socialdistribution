from backend.models import *

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import authenticate, get_user_model

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from backend.tests.payloads import *

import uuid


class TestPostViewSet(APITestCase):
    def setUp(self):
        # self.superuser = User.objects.create_superuser(
        #     'john', 'john@snow.com', 'johnpassword')

        # Why can't I use APIClient() out here?
        self.client = APIClient()

        # self.data = {'displayName': 'John',
        #              "github": "https://github.com/johnSnow",
        #              'password': 'youknownothing',
        #              'username': 'John'
        #              }

    #     self.author = Author.objects.create(**get_test_post_fields())
    #     self.post_test = Post.objects.create(
    #         **get_test_post_fields(), author=self.author)

    #     self.create_post_url = reverse('posts_create', kwargs=self.author.id)

    # def test_create_post(self):
    #     """Testing for creation of a post made by an author
    #     """
    #     response = self.client.post(self.create_post_url)

    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_create_user_payload_check(self):
    #     response = self.client.post(REGISTER_USER_URL, self.data)

    #     self.assertIn('type', response.data)
    #     self.assertIn('id', response.data)
    #     self.assertIn('host', response.data)
    #     self.assertIn('displayName', response.data)
    #     self.assertIn('url', response.data)
    #     self.assertIn('github', response.data)

    #     self.assertEqual(response.data['type'], 'author')
    #     self.assertEqual(response.data['host'], '127.0.0.1:8000')
    #     self.assertEqual(response.data['displayName'], 'John')
    #     self.assertEqual(
    #         response.data['github'], "https://github.com/johnSnow")

    # def test_get_author(self):
    #     """Testing for creation of an author
    #     """
    #     # post_response = self.client.post(
    #     #     REGISTER_USER_URL, self.data, format='json')

    #     # self.author_id = post_response.data["id"].split("/")[-1]

    #     get_response = self.client.get(
    #         f'{REGISTER_USER_URL}/{self.user_test.id}')
    #     print(get_response)
    #     print(self.user_test)

    #     # self.assertEqual(get_response.status_code, status.HTTP_200_OK)

    # def test_overwrite_author(self):
    #     payload = {'displayName': 'John',
    #                "github": "https://github.com/johnSnow",
    #                }

    #     Author.objects.create(**payload)

    #     response = self.client.post(REGISTER_USER_URL, payload)

    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
