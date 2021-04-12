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

        self.test_user4 = User.objects.create_user(
            username='bran',
            password='3eyedcrow'
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

        self.author_test3 = Author.objects.create(
            user=self.test_user3,
            displayName='Sansa Stark',
            host="http://localhost:8000/",
            github="https://www.github.com/queenofthenorth"
        )

        self.author_test4 = Author.objects.create(
            user=self.test_user4,
            displayName='Bran Stark',
            host="http://localhost:8000/",
            github="https://www.github.com/broken"
        )

        self.author_test3.save()
        self.author_test4.save()

        self.author1_follow_author2 = Follow.objects.create(
            follower=self.author_test1,
            followee=self.author_test2,
            friends=False
        )
        self.author1_follow_author2.save()

        self.author3_follow_author2 = Follow.objects.create(
            follower=self.author_test3,
            followee=self.author_test2,
            friends=False
        )
        self.author3_follow_author2.save()

        self.author3_friend_author4 = Follow.objects.create(
            follower=self.author_test3,
            followee=self.author_test4,
            friends=True
        )
        self.author3_friend_author4.save()

    def test_follow_reciprocal(self):
        """Testing for friending an author who follows them and
            checking for them as a friend
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

        response = self.client.put(
            reverse(
                'update_followers',
                kwargs={
                    'author_id': self.author_test1.id,
                    'foreign_id': self.author_test2.id
                }
            ),
            follow_request,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        """This tests for FriendsAPI that returns a list of all friends
            of an author
        """
        friend_response = self.client.get(
            reverse(
                'friends_api',
                kwargs={
                    'author_id': self.author_test1.id
                }
            )
        )

        self.assertEqual(friend_response.status_code, status.HTTP_200_OK)
        self.assertEqual(friend_response.data['items'][0]['id'].split(
            "/")[-1], self.author_test2.id)

    def test_get_follower(self):
        """
        Testing for returning a follow object if the foreign author follows
        an author regardless of them being friends
        """
        # forcing authentication of an authors
        self.client.force_authenticate(user=self.author_test1.user)
        self.client.force_authenticate(user=self.author_test2.user)

        response = self.client.get(
            reverse(
                'update_followers',
                kwargs={
                    'author_id': self.author_test2.id,
                    'foreign_id': self.author_test1.id
                }
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['type'], 'Follow')
        self.assertTrue(response.data['actor']['id'].split(
            "/")[-1], self.author_test1.id)
        self.assertEqual(response.data['object']['id'].split(
            "/")[-1], self.author_test2.id)

    def test_follow_list(self):
        """
        Testing for returning a list of all followers of an author
        """
        # forcing authentication of an authors
        self.client.force_authenticate(user=self.author_test1.user)

        response = self.client.get(
            reverse(
                'followers_list',
                kwargs={
                    'author_id': self.author_test2.id
                }
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['items'][0]['id'].split(
            "/")[-1], self.author_test1.id)
        self.assertEqual(response.data['items'][1]['id'].split(
            "/")[-1], self.author_test3.id)

    def test_get_follower(self):
        """
        Testing for deleting a friend or a follower
        """
        # forcing authentication of an authors
        self.client.force_authenticate(user=self.author_test3.user)
        self.client.force_authenticate(user=self.author_test4.user)

        response = self.client.delete(
            reverse(
                'update_followers',
                kwargs={
                    'author_id': self.author_test4.id,
                    'foreign_id': self.author_test3.id
                }
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['type'], 'Follow')
