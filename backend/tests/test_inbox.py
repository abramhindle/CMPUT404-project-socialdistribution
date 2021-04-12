from django.http import response
from backend.apis import *
from backend.models import *

from django.urls import reverse
from django.contrib.auth import authenticate, login

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

USER_LOGIN_URL = reverse('author_login')


class TestLikeAPI(APITestCase):
    def setUp(self):
        self.test_user1 = User.objects.create_user(
            username='jon',
            password='youknownothing'
        )

        self.test_user2 = User.objects.create_user(
            username='arya',
            password='nonone'
        )

        self.test_user3 = User.objects.create_user(
            username='sansa',
            password='kween'
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

        self.author_test3 = Author.objects.create(
            user=self.test_user3,
            displayName='Sansa Stark',
            host="http://localhost:8000/",
            github="https://www.github.com/queenofthenorth"
        )

        self.author_test1.save()
        self.author_test2.save()
        self.author_test3.save()

        self.test_post1_author1 = Post.objects.create(
            author=self.author_test1,
            title="I dun wannit",
            description="Jon Snow on not wanting the throne",
            content="Some plaintext for Jon",
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

        # Creating likes
        self.test_like1_post1 = Like.objects.create(
            author=self.author_test2,
            post=self.test_post1_author1,
        )
        self.test_like1_post1.save()

        self.author3_follow_author1 = Follow.objects.create(
            follower=self.author_test3,
            followee=self.author_test1,
            friends=False
        )
        self.author3_follow_author1.save()

        self.author1_inbox = Inbox.objects.create(
            author=self.author_test1,
            like=self.test_like1_post1,
            follow=self.author3_follow_author1
        )
        self.author1_inbox.save()

    def test_add_follow_request_to_inbox(self):
        """Testing for adding a follow request to the inbox of the followee author
        """
        # forcing authentication of an authors
        self.client.force_authenticate(user=self.author_test1.user)
        self.client.force_authenticate(user=self.author_test2.user)

        follow_request = {
            'type': "Follow",
            'object': {
                "type": "author",
                "id": "http://localhost:8000/author/{}".format(self.author_test1.id),
                "host": "http://localhost:8000/",
                "displayName": "Jon Snow",
                "github": "https://www.github.com/jonSnow"
            },
            'actor': {
                "type": "author",
                "id": "http://localhost:8000/author/{}".format(self.author_test2.id),
                "host": "http://localhost:8000/",
                "displayName": "Arya Stark",
                "github": "https://www.github.com/AryaStark"
            }
        }

        response = self.client.post(
            reverse(
                'inbox_object',
                kwargs={
                    'author_id': self.author_test1.id
                }
            ),
            follow_request,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_inbox(self):
        """
        Testing for returning the inbox of an author
        """
        # forcing authentication of an authors
        self.client.force_authenticate(user=self.author_test1.user)

        response = self.client.get(
            reverse(
                'inbox_object',
                kwargs={
                    'author_id': self.author_test1.id,
                }
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(response.data['items'][0]['type'], "Like")
        self.assertTrue(response.data['items'][1]['type'], "Follow")

    def test_delete_inbox(self):
        """
        Testing for deleting the inbox of an author
        """
        # forcing authentication of an authors
        self.client.force_authenticate(user=self.author_test1.user)

        response = self.client.delete(
            reverse(
                'inbox_object',
                kwargs={
                    'author_id': self.author_test1.id,
                }
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
