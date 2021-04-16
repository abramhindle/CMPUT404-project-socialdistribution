from django.http import response
from backend.apis import *
from backend.models import *

from django.urls import reverse
from django.contrib.auth import authenticate, login

from rest_framework.test import APIClient, APITestCase
from rest_framework import status


class TestNodeEndpoints(APITestCase):
    def setUp(self):
        self.test_user1 = User.objects.create_user(
            username='jon',
            password='youknownothing'
        )

        self.test_user2 = User.objects.create_user(
            username='arya',
            password='nonone'
        )

        self.client1 = APIClient(
            HTTP_HOST='127.0.0.1:8000')
        self.client2 = APIClient(
            HTTP_HOST='9.228.99.132:8080')

        self.author_test_local = Author.objects.create(
            user=self.test_user1,
            displayName='Jon Snow',
            host="http://localhost:8000/",
            github="https://www.github.com/johnSnow"
        )

        self.author_test_remote = Author.objects.create(
            user=self.test_user2,
            displayName='Arya Stark',
            host="http://9.228.99.132:8080/",
            github="https://www.github.com/AryaStark"
        )

        self.author_test_local.save()
        self.author_test_remote.save()

    def test_follow_remote_user(self):
        """Testing for a sending a follow request to a remote author
        """
        # forcing authentication of an authors
        self.client1.force_authenticate(user=self.author_test_local.user)
        self.client1.force_authenticate(user=self.author_test_remote.user)

        follow_request = {
            'type': "Follow",
            'object': {
                "type": "author",
                "id": "http://localhost:8000/author/{}".format(self.author_test_local.id),
                "host": "http://localhost:8000/",
                "displayName": "Jon Snow",
                "github": "https://www.github.com/jonSnow"
            },
            'actor': {
                "type": "author",
                "id": "http://9.228.99.132:8080/author/{}".format(self.author_test_remote.id),
                "host": "http://9.228.99.132:8080/",
                "displayName": "Arya Stark",
                "github": "https://www.github.com/AryaStark"
            }
        }

        self.mock_remote_node = Node.objects.create(
            host="http://9.228.99.132:8080/",
            user=self.author_test_remote.user,
            remote_username='jon',
            remote_password='youknownothing'
        )
        self.mock_remote_node.save()

        response = self.client1.put(
            reverse(
                'update_followers',
                kwargs={
                    'author_id': self.author_test_local.id,
                    'foreign_id': self.author_test_remote.id
                }
            ),
            follow_request,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unsuccessful_follow_remote_user(self):
        """Testing for a sending a follow request to a remote author
        """
        # forcing authentication of an authors
        self.client1.force_authenticate(user=self.author_test_local.user)
        self.client1.force_authenticate(user=self.author_test_remote.user)

        follow_request = {
            'type': "Follow",
            'object': {
                "type": "author",
                "id": "http://localhost:8000/author/{}".format(self.author_test_local.id),
                "host": "http://localhost:8000/",
                "displayName": "Jon Snow",
                "github": "https://www.github.com/jonSnow"
            },
            'actor': {
                "type": "author",
                "id": "http://9.228.99.132:8080/author/{}".format(self.author_test_remote.id),
                "host": "http://9.228.99.132:8080/",
                "displayName": "Arya Stark",
                "github": "https://www.github.com/AryaStark"
            }
        }

        self.mock_remote_node = Node.objects.create(
            host="http://9.228.99.132:8080/",
            user=self.author_test_remote.user,
            remote_username='jacob',
            remote_password='whydodis'
        )
        self.mock_remote_node.save()

        response = self.client1.put(
            reverse(
                'update_followers',
                kwargs={
                    'author_id': self.author_test_local.id,
                    'foreign_id': self.author_test_remote.id
                }
            ),
            follow_request,
            format='json'
        )
        self.assertNotEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
