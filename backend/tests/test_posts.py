from backend.apis import *
from backend.models import *

from django.urls import reverse
from django.contrib.auth import authenticate, login

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from backend.tests.payloads import *

USER_LOGIN_URL = reverse('author_login')


class TestPostViewSet(APITestCase):
    def setUp(self):
        self.test_user1 = User.objects.create_user(
            username='jon',
            password='youknownothing'
        )

        self.test_user2 = User.objects.create_user(
            username='arya',
            password='nonone'
        )

        self.client = APIClient()

        self.author_test1 = Author.objects.create(
            user=self.test_user1,
            displayName='Jon Snow',
            host="http://localhost:8000/",
            github="https://www.github.com/johnSnow"
        )

        self.author_test2 = Author.objects.create(
            user=self.test_user2,
            displayName='Arya Stark',
            host="http://localhost:8000/",
            github="https://www.github.com/AryaStark"
        )

        self.author_test1.save()
        self.author_test2.save()

        # Login both users
        test_login_data1 = {
            'username': 'jon',
            'password': 'youknownothing',
        }
        test_login_data2 = {
            'username': 'arya',
            'password': 'noone',
        }

        # Logging into authors
        login_response1 = self.client.post(
            USER_LOGIN_URL, test_login_data1, format='json')
        login_response2 = self.client.post(
            USER_LOGIN_URL, test_login_data2, format='json')

        # Make User 1 create a POST
        self.test_post1_author1 = Post.objects.create(
            author=self.author_test1,
            title="I dun wannit",
            description="Jon Snow on not wanting the throne",
            content="Some plaintext",
            contentType="text/plain",
            visibility="PUBLIC",
            unlisted=False,
            categories=[
                "Test",
                "post",
                "author"
            ],
        )

        self.test_post1_author1.save()

    def test_create_post(self):
        """Testing for creation of a post made by an author
        """

        self.client.force_authenticate(user=self.author_test1.user)

        create_request = {
            "type": "post",
            "title": "This is the third best post of all time",
            "description": "this is a text post",
            "contentType": "text/plain",
            "content": "This is some text that goes in the post body",
            "categories": [
                "Test",
                "post",
                "author"
            ],
            "visibility": "PUBLIC",
            "unlisted": False,
            "author": self.author_test1
        }

        response = self.client.post(
            reverse('posts_object', kwargs={'author_id': self.author_test1.id}), create_request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_check_post_list(self):
        """Testing for returning a list of all public posts made by author
        """
        self.client.force_authenticate(user=self.author_test1.user)

        list_response = self.client.get(
            reverse('posts_object', kwargs={'author_id': self.author_test1.id}))

        self.assertEqual(list_response.status_code, status.HTTP_200_OK)

        self.assertEqual(list_response.data[0]['type'], 'post')
        self.assertEqual(list_response.data[0]['title'], 'I dun wannit')

        self.assertEqual(list_response.data[1]['type'], 'post')
        self.assertEqual(
            list_response.data[1]['title'], 'This is the third best post of all time')
