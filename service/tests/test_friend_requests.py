from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from dashboard.models import Node, Author


class FriendRequestsTestCase(APITestCase):
    def setUp(self):
        self.node = Node.objects.create(name="Test", host="http://www.socdis.com/",
                                        service_url="http://api.socdis.com/")

        self.author = Author.objects.create(node=self.node, displayName="Test 1", activated=True)
        self.friend = Author.objects.create(node=self.node, displayName="Test 2", activated=True)

    def test_friend_request(self):
        url = reverse('friend-request')

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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
