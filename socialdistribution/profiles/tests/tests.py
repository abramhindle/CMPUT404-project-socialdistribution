import uuid
from django.test import TestCase
from profiles.models import Author
from profiles.utils import getAuthorFriendRelationships, getFriendsOfAuthor,\
                    getFriendRequestsToAuthor, getFriendRequestsFromAuthor,\
                    isFriend

# from django.utils import timezone
# from django.core.urlresolvers import reverse
# from whatever.forms import WhateverForm


# models test
class ProfilesTest(TestCase):

    def create_author(self, uuid_id, email, firstName, lastName, displayName, bio, host, github, password):
        return Author.objects.create(id=uuid_id, email=email, firstName=firstName,lastName=lastName,
                                     displayName=displayName, host=host, github=github, password=password)

    def test_author_creation(self):
        uuid_id = uuid.uuid4()
        email = "test@gmail.com"
        firstName = "TestFirst"
        lastName = "TestLast"
        displayName = "Test Display Name"
        bio = "Test bio"
        host = "http://testhost:1234"
        github = "https//testgithub.com"
        password = "testPassword"
        author = self.create_author(uuid_id, email, firstName, lastName, displayName, bio, host, github, password)
        self.assertTrue(isinstance(author, Author))
        self.assertEqual(author.url, host+"/author/"+str(uuid_id))
        self.assertEqual(author.__str__(), firstName+" "+lastName)

    def test_get_author_friend_relationships(self):
        pass

    def test_get_friends_of_author(self):
        pass

    def test_get_friend_request_to_author(self):
        pass

    def test_get_friend_requests_from_author(self):
        pass

    def test_is_friend(self):
        pass

    def test_accept_friend(self):
        pass

    def test_reject_friend(self):
        pass

    def test_my_friends(self):
        pass

    def test_my_friend_requests(self):
        pass

    def test_my_friend_following(self):
        pass

    def test_view_author_profile(self):
        pass

    def view_profile(self):
        pass

    def edit_profile(self):
        pass

    def new_post(self):
        pass
# Create your tests here.
