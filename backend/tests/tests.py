from backend.models import *

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import authenticate, get_user_model

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from backend.tests.payloads import *

import uuid


# class UserTestCase(TestCase):
#     def setUp(self):
#         user = User.objects.create_user(
#             username='testDude', password='testpassword')
#         self.testUser = Author.objects.create(
#             id=generate_uuid, user=user, displayName="TestDude")
#         self.testUser.save()

#     def test_display_name(self):
#         # tests that when a user sets their display name it doesnt default back to the username
#         user = Author.objects.get(displayName="TestDude")
#         self.assertEqual(user.displayName, "TestDude")

#     # def test_response_code(self):
#     #     # Tests reponse codes returned by creation of a author

#     def tearDown(self):
#         self.testUser.delete()


# class AuthorTestCase(TestCase):
#     def setUp(self):
#         user = User.objects.create_user(
#             username='testDude', password='testpassword')
#         self.testUser = Author.objects.create(
#             id=generate_uuid, user=user, displayName="TestDude")
#         self.testUser.save()


# class LoginTestCase(TestCase):
#     def setUp(self):
#         user = User.objects.create_user(
#             'test_dude', 'test@email.com', 'test_password')
#         self.nervousTestMan = Author.objects.create(
#             id=generate_uuid, user=user, displayName="test_dude")
#         self.nervousTestMan.save()

#     def test_correct(self):
#         # Tests whether authentication passes with correct credentials
#         user = authenticate(username='nervousMan', password='test_password')
#         self.assertTrue((user is not None) and user.is_authenticated)

#     def test_incorrect_username(self):
#         # Tests whether authentication does not pass with incorrect username
#         user = authenticate(username='incorect_username',
#                             password='test_password')
#         self.assertFalse(user is not None and user.is_authenticated)

#     def test_incorrect_password(self):
#         # Tests whether authentication does not pass with incorrect password
#         user = authenticate(username='test_dude', password='wrong_password')
#         self.assertFalse(user is not None and user.is_authenticated)

#     def test_update_info(self):
#         request=

#     def tearDown(self):
#         self.nervousTestMan.delete()

REGISTER_USER_URL = reverse('author_register')


class TestRegisterAuthor(APITestCase):
    def setUp(self):
        # self.superuser = User.objects.create_superuser(
        #     'john', 'john@snow.com', 'johnpassword')

        # Why can't I use APIClient() out here?
        self.client = Client(
            HTTP_HOST='127.0.0.1:8000',
            ALLOWED_HOSTS='127.0.0.1'
        )

        self.data = {'displayName': 'John',
                     "github": "https://github.com/johnSnow",
                     'password': 'youknownothing',
                     'username': 'John'
                     }

        self.user_test = Author.objects.create(**get_test_author_fields())

    def test_create_author(self):
        """Testing for creation of an author
        """
        response = self.client.post(REGISTER_USER_URL, self.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user_payload_check(self):
        response = self.client.post(REGISTER_USER_URL, self.data)

        self.assertIn('type', response.data)
        self.assertIn('id', response.data)
        self.assertIn('host', response.data)
        self.assertIn('displayName', response.data)
        self.assertIn('url', response.data)
        self.assertIn('github', response.data)

        self.assertEqual(response.data['type'], 'author')
        self.assertEqual(response.data['host'], '127.0.0.1:8000')
        self.assertEqual(response.data['displayName'], 'John')
        self.assertEqual(
            response.data['github'], "https://github.com/johnSnow")

    def test_get_author(self):
        """Testing for creation of an author
        """
        # post_response = self.client.post(
        #     REGISTER_USER_URL, self.data, format='json')

        # self.author_id = post_response.data["id"].split("/")[-1]

        get_response = self.client.get(
            f'{REGISTER_USER_URL}/{self.user_test.id}')
        print(get_response)
        print(self.user_test)

        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

    def test_overwrite_author(self):
        payload = {'displayName': 'John',
                   "github": "https://github.com/johnSnow",
                   }

        Author.objects.create(**payload)

        response = self.client.post(REGISTER_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)\
