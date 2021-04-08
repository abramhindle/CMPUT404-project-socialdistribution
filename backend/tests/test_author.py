from backend.models import *
from backend.tests.payloads import *

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import authenticate, get_user_model

from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import serializers, status
from rest_framework.decorators import action

from ..serializers import AuthorSerializer, RegisterSerializer


USER_LOGIN_URL = reverse('author_login')


class TestAuthorViewSet(APITestCase):
    def setUp(self):
        test_user = User.objects.create_user(
            username='john',
            password='youknownothing'
        )

        self.client = APIClient()

        self.login_data = {
            'username': 'john',
            'password': 'youknownothing',
        }

        self.author_test = Author.objects.create(
            user=test_user,
            displayName='John',
            host="http://localhost:8000/",
            github="https://www.github.com/johnSnow"
        )
        self.author_test.save()

    def test_login_author(self):
        """Testing for login of an author
        """
        # Logging into author
        login_response = self.client.post(
            USER_LOGIN_URL, self.login_data, format='json')

        # checking for authorized user
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

    def test_retrieve_author(self):
        """Testing for login of an author
        """
        # forcing authentication of an author
        self.client.force_authenticate(user=self.author_test.user)

        # getting an author
        author_response = self.client.get(
            reverse('author_object', kwargs={'id': self.author_test.id}))

        # checking for authorized user
        self.assertEqual(author_response.status_code, status.HTTP_200_OK)

    # # def test_overwrite_author(self):
    #     # payload = {
    #     #     'displayName': 'John',
    #     #     "github": "https://github.com/johnSnow",
    #     # }

    #     # Author.objects.create(**payload)

    #     # response = self.client.post(REGISTER_USER_URL, payload)

    #     # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
