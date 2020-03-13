import uuid
from django.test import TestCase
from profiles.models import Author, AuthorFriend
from faker import Faker
from profiles.utils import getAuthorFriendRelationships, getFriendsOfAuthor,\
                    getFriendRequestsToAuthor, getFriendRequestsFromAuthor,\
                    isFriend
from django.test import Client
from django.contrib.auth import get_user_model

# from django.utils import timezone
# from django.core.urlresolvers import reverse
# from whatever.forms import WhateverForm

faker = Faker()


# models test
class ProfilesTest(TestCase):

    def create_author(self):
        uuid_id = uuid.uuid4()
        email = faker.email()
        firstName = faker.first_name()
        lastName = faker.last_name()
        displayName = firstName + lastName
        bio = faker.text()
        host = faker.hostname()
        github = "https://github.com/" + displayName
        password = "testPassword"

        return Author.objects.create(id=uuid_id, email=email,
                                     firstName=firstName, lastName=lastName,
                                     displayName=displayName, bio=bio,
                                     host=host, github=github,
                                     password=password)

    def create_author_friend(self, author=None,
                             friend=None):
        if not author:
            author = self.create_author()
        if not friend:
            friend = self.create_friend()

        return AuthorFriend.objects.create(author=author, friend=friend)

    def test_author_creation(self):
        author = self.create_author()

        self.assertTrue(isinstance(author, Author))
        self.assertEqual(author.url, author.host+"/author/"+str(author.id))
        self.assertEqual(author.__str__(), author.firstName+" "+author.lastName)

    def test_author_friend_creation(self):
        author = self.create_author()
        friend = self.create_author()
        author_friend = self.create_author_friend(author, friend)

        self.assertTrue(isinstance(author_friend, AuthorFriend))
        self.assertEqual(author_friend.author, author)
        self.assertEqual(author_friend.friend, friend)

    def test_get_author_friend_relationships(self):
        author1 = self.create_author()
        author2 = self.create_author()
        author3 = self.create_author()
        author1_author2 = AuthorFriend.objects.create(author=author1, friend=author2)
        author2_author3 = AuthorFriend.objects.create(author=author2, friend=author3)
        author2_friends, friends_author2 = getAuthorFriendRelationships(author2)

        self.assertIn(author2_author3, author2_friends)
        self.assertIn(author1_author2, friends_author2)

    def test_get_friends_of_author(self):
        author1 = self.create_author()
        author2 = self.create_author()
        author3 = self.create_author()
        AuthorFriend.objects.create(author=author1, friend=author2)
        AuthorFriend.objects.create(author=author2, friend=author1)
        AuthorFriend.objects.create(author=author3, friend=author2)
        author2_friends = getFriendsOfAuthor(author2)

        # We should be returning a query object, but right now it is a list
        # Should refactor moving forward
        author2_friends_with_author1 = False
        author2_friends_with_author3 = False
        for author_friend in author2_friends:
            if author1 == author_friend.friend:
                author2_friends_with_author1 = True
            if author3 == author_friend.friend:
                author2_friends_with_author3 = True

        self.assertTrue(author2_friends_with_author1)
        self.assertFalse(author2_friends_with_author3)

    def test_get_friend_request_to_author(self):
        author1 = self.create_author()
        author2 = self.create_author()
        author3 = self.create_author()
        AuthorFriend.objects.create(author=author1, friend=author2)
        AuthorFriend.objects.create(author=author2, friend=author1)
        AuthorFriend.objects.create(author=author3, friend=author2)
        author2_friend_requests = getFriendRequestsToAuthor(author2)

        # We should be returning a query object, but right now it is a list
        # Should refactor moving forward
        author1_friend_request_to_author2 = False
        author3_friend_request_to_author2 = False
        for author_friend in author2_friend_requests:
            if author1 == author_friend.author:
                author1_friend_request_to_author2 = True
            if author3 == author_friend.author:
                author3_friend_request_to_author2 = True

        self.assertFalse(author1_friend_request_to_author2)
        self.assertTrue(author3_friend_request_to_author2)

    def test_get_friend_requests_from_author(self):
        author1 = self.create_author()
        author2 = self.create_author()
        author3 = self.create_author()
        AuthorFriend.objects.create(author=author1, friend=author2)
        AuthorFriend.objects.create(author=author2, friend=author1)
        AuthorFriend.objects.create(author=author3, friend=author2)
        author3_sent_friend_requests = getFriendRequestsFromAuthor(author3)

        # We should be returning a query object, but right now it is a list
        # Should refactor moving forward
        author3_friend_request_to_author2 = False
        author3_friend_request_to_author1 = False
        for author_friend in author3_sent_friend_requests:
            if author2 == author_friend.friend:
                author3_friend_request_to_author2 = True
            if author1 == author_friend.friend:
                author3_friend_request_to_author2 = True

        self.assertTrue(author3_friend_request_to_author2)
        self.assertFalse(author3_friend_request_to_author1)

    def test_is_friend(self):
        author1 = self.create_author()
        author2 = self.create_author()
        author3 = self.create_author()
        AuthorFriend.objects.create(author=author1, friend=author2)
        AuthorFriend.objects.create(author=author2, friend=author1)
        AuthorFriend.objects.create(author=author3, friend=author2)

        self.assertTrue(isFriend(author1, author2))
        self.assertFalse(isFriend(author2, author3))

    def test_view_login(self):
        c = Client()
        response = c.get('http://127.0.0.1:8000/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_account_login(self):
        account = get_user_model()
        account.objects.create_superuser('to@to.com', 'wrongaccount')
        client = Client()

        # Logging in, and retreiving stream (can only do when logged in)
        client.login(email='to@to.com', password='wrongaccount')
        login_stream = client.get('/accounts/password_change/')
        self.assertTrue(login_stream.status_code == 200)

        # Logout, and retreive stream (returns HTTP 302 to redirect to /accounts/login)
        client.get('/accounts/logout/')
        logout_stream = client.get('/accounts/password_change/')
        self.assertTrue(logout_stream.status_code == 302)
        self.assertTrue("/accounts/login" in logout_stream.url)
    # Will implement view tests in the future

    def test_accept_friend(self):
        pass

    # Will implement view tests in the future
    def test_reject_friend(self):
        pass

    # Will implement view tests in the future
    def test_my_friends(self):
        pass

    # Will implement view tests in the future
    def test_my_friend_requests(self):
        pass

    # Will implement view tests in the future
    def test_my_friend_following(self):
        pass

    # Will implement view tests in the future
    def test_view_author_profile(self):
        pass

    # Will implement view tests in the future
    def test_view_profile(self):
        pass

    # Will implement view tests in the future
    def test_edit_profile(self):
        pass

    # Will implement view tests in the future
    def test_new_post(self):
        pass
# Create your tests here.
