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


class TestAuthorViewSet(APITestCase):
    def setUp(self):
        # self.superuser = User.objects.create_superuser(
        #     'john', 'john@snow.com', 'johnpassword')

        # Why can't I use APIClient() out here?
        self.client = APIClient()

        self.data = {'displayName': 'John',
                     "github": "https://github.com/johnSnow",
                     'password': 'youknownothing',
                     'username': 'John'
                     }

        self.author_test = Author.objects.create(**get_test_author_fields())

    @action(detail=True, methods=['post', 'get'], permission_classes=[IsAuthenticated])
    def test_get_author(self):
        """Testing for creation of an author
        """
        # post_response = self.client.post(
        #     REGISTER_USER_URL, self.data, format='json')

        # self.author_id = post_response.data["id"].split("/")[-1]

        # serializer_test = RegisterSerializer.create()
        # serializer_test.is_valid(raise_exception=True)
        # user_test = serializer_test.save()
        # token = Token.objects.create(user=user_test)

        get_response = self.client.get(
            reverse('author_object', kwargs={'id': self.author_test.id}))

        # author = Author.objects.filer(id=self.user_test.id)
        # serializer = AuthorSerializer(author)
        # print(serializer.data)
        print(get_response)

        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

    # def test_overwrite_author(self):
        # payload = {
        #     'displayName': 'John',
        #     "github": "https://github.com/johnSnow",
        # }

        # Author.objects.create(**payload)

        # response = self.client.post(REGISTER_USER_URL, payload)

        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
