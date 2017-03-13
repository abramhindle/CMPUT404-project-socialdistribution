from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from dashboard.models import Node, Author


class FriendRequestTestCase(APITestCase):
    def setUp(self):
        self.node = Node.objects.create(name="Test", host="http://www.socdis.com/",
                                        service_url="http://api.socdis.com/", local=True)

        user1 = User.objects.create_user("test1", "test@test.com", "pass1")
        user2 = User.objects.create_user("test2", "test@test.com", "pass2")

        self.author = Author.objects.get(user__id=user1.id)
        self.author.activated = True
        self.author.save()
        self.friend = Author.objects.get(user__id=user2.id)

    def test_friend_requests(self):
        self.client.login(username="test1", password="pass1")

        url = reverse('service:friend-request')

        data = {
            "query": "friendrequest",
            "author": {
                "id": "http://api.socdis.com/author/%s" % self.author.id,
                "host": "http://api.socdis.com/",
                "displayName": "Greg Johnson",
                "url": "http://api.socdis.com/author/%s" % self.author.id,
            },
            "friend": {
                "id": "http://api.socdis.com/author/%s" % self.friend.id,
                "host": "http://api.socdis.com/",
                "displayName": "Lara Croft",
                "url": "http://api.socdis.com/author/%s" % self.friend.id,
            }
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

        self.assertTrue(self.author.has_outgoing_friend_request_for(self.friend))
        self.assertTrue(self.friend.has_incoming_friend_request_from(self.author))
        self.assertTrue(self.author.follows(self.friend))

    def test_unauthed_friend_request_fails(self):
        url = reverse('service:friend-request')

        data = {
            "query": "friendrequest",
            "author": {
                "id": "http://api.socdis.com/author/%s" % self.author.id,
                "host": "http://api.socdis.com/",
                "displayName": "Greg Johnson",
                "url": "http://api.socdis.com/author/%s" % self.author.id,
            },
            "friend": {
                "id": "http://api.socdis.com/author/%s" % self.friend.id,
                "host": "http://api.socdis.com/",
                "displayName": "Lara Croft",
                "url": "http://api.socdis.com/author/%s" % self.friend.id,
            }
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

