from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from follow.admin import AddFriendAction

from .models import Follow


class FriendRequestsViewTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.bob = get_user_model().objects.create_user(username='bob', password='password')
        self.alice = get_user_model().objects.create_user(username='alice', password='password')

    def test_friend_requests_page(self):
        self.client.login(username='bob', password='password')
        res = self.client.get(reverse('follow:friend_requests'))

        self.assertTemplateUsed(res, 'follow/request_list.html')

    def test_friend_requests(self):
        Follow.objects.follow_request(from_user=self.alice, to_user=self.bob)
        self.client.login(username='bob', password='password')
        res = self.client.get(reverse('follow:friend_requests'))

        self.assertContains(res, self.alice.username)


class AddFriendActionTests(TestCase):
    def setUp(self) -> None:
        self.bob = get_user_model().objects.create_user(username='bob', password='password')
        self.alice = get_user_model().objects.create_user(username='alice', password='password')

    def test_add_friend_enable_default(self):
        self.assertIsNotNone(AddFriendAction(self.bob, self.alice))

    def test_disabled_when_requested_already(self):
        Follow.objects.follow_request(from_user=self.bob, to_user=self.alice)
        self.assertIsNone(AddFriendAction(self.bob, self.alice))

    def test_disabled_when_following_already(self):
        request = Follow.objects.follow_request(from_user=self.bob, to_user=self.alice)
        request.accept()
        self.assertIsNone(AddFriendAction(self.bob, self.alice))


class FollowModelTests(TestCase):
    def setUp(self) -> None:
        self.bob = get_user_model().objects.create_user(username='bob', password='password')
        self.alice = get_user_model().objects.create_user(username='alice', password='password')

    def test_unfollow_request(self):
        Follow.objects.follow_request(from_user=self.bob, to_user=self.alice).accept()
        Follow.objects.follow_request(from_user=self.alice, to_user=self.bob).accept()
        self.assertEqual(len(Follow.objects.true_friend(self.bob)), 1)
        self.assertEqual(len(Follow.objects.true_friend(self.alice)), 1)

        self.assertTrue(Follow.objects.unfollow(follower=self.bob, followee=self.alice))

        self.assertEqual(len(Follow.objects.true_friend(self.bob)), 0)
        self.assertEqual(len(Follow.objects.true_friend(self.alice)), 0)
