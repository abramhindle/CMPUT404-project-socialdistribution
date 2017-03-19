from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from social.app.models.node import Node


class FollowTestCase(APITestCase):
    def setUp(self):
        node = Node.objects.create(name="Test", host="http://www.socdis.com/",
                                   service_url="http://api.socdis.com/", local=True)

        user1 = User.objects.create_user("test1", "test@test.com", "pass1")
        user2 = User.objects.create_user("test2", "test@test.com", "pass2")

        self.follower = user1.profile
        self.follower.node = node
        self.follower.save()

        self.followee = user2.profile
        self.followee.node = node
        self.followee.save()

        self.url = reverse("service:author-follow", args=[self.followee.id])

    def test_following_without_session_auth_fails(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")
        self.assertFalse(self.follower.follows(self.followee))

    def test_following_while_unactivated_fails(self):
        self.client.login(username="test1", password="pass1")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "Unactivated authors cannot follow other authors.")
        self.assertFalse(self.follower.follows(self.followee))

    def test_following_an_author_that_does_not_exist_fails(self):
        self.follower.activated = True
        self.follower.save()

        self.followee.delete()

        self.client.login(username="test1", password="pass1")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], "The author you wanted to follow could not be found.")

    def test_following_an_unactivated_author_fails(self):
        self.follower.activated = True
        self.follower.save()

        self.client.login(username="test1", password="pass1")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "Unactivated authors cannot be followed.")
        self.assertFalse(self.follower.follows(self.followee))

    def test_following_a_local_unfollowed_author_that_does_not_follow_you_succeeds(self):
        self.follower.activated = True
        self.follower.save()

        self.followee.activated = True
        self.followee.save()

        self.client.login(username="test1", password="pass1")

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_value = response.data["followed_author"]
        expected_end = reverse("service:author-detail", args=[self.followee.id])

        self.assertTrue(
            response_value.endswith(expected_end),
            msg="%s does not end with %s." % (response_value, expected_end))

        self.assertTrue(self.follower.follows(self.followee))

    def test_following_a_local_unfollowed_author_that_does_follow_you_succeeds(self):
        self.follower.activated = True
        self.follower.save()

        self.followee.activated = True
        self.followee.followed_authors.add(self.follower)
        self.followee.save()

        self.client.login(username="test1", password="pass1")

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_value = response.data["followed_author"]
        expected_end = reverse("service:author-detail", args=[self.followee.id])

        self.assertTrue(
            response_value.endswith(expected_end),
            msg="%s does not end with %s." % (response_value, expected_end))

        self.assertTrue(self.follower.follows(self.followee))

    def test_follow_a_local_already_followed_author_fails(self):
        self.follower.activated = True
        self.follower.followed_authors.add(self.followee)
        self.follower.save()

        self.followee.activated = True
        self.followee.save()

        self.assertTrue(self.follower.follows(self.followee))

        self.client.login(username="test1", password="pass1")

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "You already follow this author.")
        self.assertTrue(self.follower.follows(self.followee))
