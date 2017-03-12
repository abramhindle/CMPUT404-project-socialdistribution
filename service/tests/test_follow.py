from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from dashboard.models import Node, Author


class FollowTestCase(APITestCase):
    def setUp(self):
        self.node = Node.objects.create(name="Test", host="http://www.socdis.com/",
                                        service_url="http://api.socdis.com/", local=True)

        user1 = User.objects.create_user("test1", "test@test.com", "pass1")
        user2 = User.objects.create_user("test2", "test@test.com", "pass2")

        self.follower = Author.objects.get(user__id=user1.id)
        self.follower.activated = True
        self.follower.save()
        self.followee = Author.objects.get(user__id=user2.id)

        self.url = reverse("service:author-follow", args=[self.followee.id])

    def test_following_without_session_auth_fails(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

    def test_following_while_unactivated_fails(self):
        self.client.login(username="test1", password="pass1")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "Unactivated authors cannot follow other authors.")

    def test_following_an_unactivated_author_fails(self):
        pass

    def test_following_a_local_unfollowed_author_that_does_not_follow_you_succeeds(self):
        pass

    def test_following_a_local_unfollowed_author_that_does_follow_you_succeeds(self):
        pass

    def test_follow_a_local_already_followed_author_fails(self):
        pass
