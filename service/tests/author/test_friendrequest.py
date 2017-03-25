from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from social.app.models.node import Node


class AuthorFriendRequestTestCase(APITestCase):
    def setUp(self):
        Node.objects.create(name="Test", host="http://www.socdis.com/",
                            service_url="http://api.socdis.com/", local=True)

        user1 = User.objects.create_user("test1", "test@test.com", "pass1")
        user2 = User.objects.create_user("test2", "test@test.com", "pass2")

        self.author = user1.profile
        self.target = user2.profile

        self.url = reverse("service:author-friendrequest", args=[self.target.id])

    def test_requesting_without_session_auth_fails(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")
        self.assertFalse(self.author.has_outgoing_friend_request_for(self.target))
        self.assertFalse(self.target.has_incoming_friend_request_from(self.author))

    def test_requesting_while_unactivated_fails(self):
        self.client.login(username="test1", password="pass1")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "Unactivated authors cannot friend request other authors.")
        self.assertFalse(self.author.has_outgoing_friend_request_for(self.target))
        self.assertFalse(self.target.has_incoming_friend_request_from(self.author))

    def test_requesting_an_author_that_does_not_exist_fails(self):
        self.author.activated = True
        self.author.save()

        self.target.delete()

        self.client.login(username="test1", password="pass1")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], "The author you wanted to friend request could not be found.")

    def test_requesting_a_friend_fails(self):
        self.author.activated = True
        self.author.friends.add(self.target)
        self.author.save()

        self.target.activated = True
        self.target.save()

        self.client.login(username="test1", password="pass1")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "You are already friends with this author.")
        self.assertFalse(self.author.has_outgoing_friend_request_for(self.target))
        self.assertFalse(self.target.has_incoming_friend_request_from(self.author))

    def test_requesting_an_author_with_whom_you_already_have_a_request_fails(self):
        self.author.activated = True
        self.author.outgoing_friend_requests.add(self.target)
        self.author.save()

        self.target.activated = True
        self.target.save()

        self.client.login(username="test1", password="pass1")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "You already have a pending friend request with this author.")
        self.assertTrue(self.author.has_outgoing_friend_request_for(self.target))
        self.assertTrue(self.target.has_incoming_friend_request_from(self.author))

    def test_requesting_an_author_succeeds_and_also_follows_them(self):
        self.author.activated = True
        self.author.save()

        self.target.activated = True
        self.target.save()

        self.client.login(username="test1", password="pass1")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_value = response.data["friend_requested_author"]
        expected_end = reverse("service:author-detail", args=[self.target.id])

        self.assertTrue(
            response_value.endswith(expected_end),
            msg="%s does not end with %s." % (response_value, expected_end))

        self.assertTrue(self.author.has_outgoing_friend_request_for(self.target))
        self.assertTrue(self.target.has_incoming_friend_request_from(self.author))
        self.assertTrue(self.author.follows(self.target))
