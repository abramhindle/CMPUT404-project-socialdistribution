from django.urls import reverse
from rest_framework import status
from posts.views import FrontEndUserEditView
from posts.models import User
from preferences import preferences
from posts.serializers import UserSerializer
from django.test import Client
from posts.tests import factory
from django.test import TestCase
from django.db import transaction
from django.forms.models import model_to_dict


class UserTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.helper_functions = factory.GeneralFunctions()

    def test_user_update_valid_username_from_post(self):
        password = 'password123'
        user = self.helper_functions.create_user(password=password)
        old_data = UserSerializer(user).data
        url = reverse('edit_user')
        self.client.login(username=user.username, password=password)

        original_username = old_data['displayName']
        new_username = original_username + '_EDITED'
        data = {'username': new_username}

        response = self.client.post(url, data=data)

        updated_user = User.objects.get(username=new_username)
        new_data = UserSerializer(updated_user).data

        with self.assertRaises(User.DoesNotExist):
            old_user = User.objects.get(username=original_username)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertNotEqual(old_data['displayName'], new_data['displayName'])
        old_data.pop('displayName'), new_data.pop('displayName')
        self.assertEqual(old_data, new_data)


    def test_user_update_invalid_username_from_post(self):
        a_pass = 'alice_password'
        alice = self.helper_functions.create_user(username="alice", password=a_pass)
        alice_old_data = UserSerializer(alice).data
        b_pass = 'bob_password'
        bob = self.helper_functions.create_user(username="bob", password=b_pass)
        bob_old_data = UserSerializer(bob).data
        url = reverse('edit_user')
        self.client.login(username=alice.username, password=a_pass)

        alice_new_username = 'bob'
        data = {'username': alice_new_username}
        with transaction.atomic():
            response = self.client.post(url, data=data)

        alice = User.objects.get(username='alice')
        alice_new_data = UserSerializer(alice).data
        bob = User.objects.get(username='bob')
        bob_new_data = UserSerializer(bob).data

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(alice_old_data, alice_new_data)
        self.assertEqual(bob_old_data, bob_new_data)


    def test_user_update_valid_email_from_post(self):
        password = 'P455w0rd123!'
        user = self.helper_functions.create_user(password=password)
        old_data = UserSerializer(user).data
        url = reverse('edit_user')
        self.client.login(username=user.username, password=password)

        old_email = user.email
        new_email = old_email.split('@')[0] + '_FOO' + old_email.split('@')[1]
        data = {'email':new_email}
        with transaction.atomic():
            response = self.client.post(url, data=data)

        updated_user = User.objects.get(username=user.username)
        new_data = UserSerializer(updated_user).data

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertNotEqual(old_data['email'], new_data['email'])
        old_data.pop('email'), new_data.pop('email')
        self.assertEqual(old_data, new_data)


    # NOTE: multiple users can share same email currently, so this test will fail
    # def test_user_update_invalid_email_from_post(self):
    #     password = 'P455w0rd123!'
    #     alice = self.helper_functions.create_user(username='alice', password=password, email="alice@email.com")
    #     bob = self.helper_functions.create_user(username='bob', password=password, email="bob@email.com")
    #
    #     url = reverse('edit_user')
    #     self.client.login(username=alice.username, password=password)
    #
    #     old_email = alice.email
    #     new_email = bob.email
    #     data = {'email':new_email}
    #
    #     with transaction.atomic():
    #         response = self.client.post(url, data=data)
    #
    #     updated_user = User.objects.get(username=alice.username)
    #
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(updated_user.email, old_email)


    def test_user_update_valid_github_from_post(self):
        password = 'P455w0rd123!'
        user = self.helper_functions.create_user(password=password)
        old_data = UserSerializer(user).data
        url = reverse('edit_user')
        self.client.login(username=user.username, password=password)

        new_github = 'npwhite'
        data = {'github':new_github}
        with transaction.atomic():
            response = self.client.post(url, data=data)

        updated_user = User.objects.get(username=user.username)
        new_data = UserSerializer(updated_user).data

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertNotEqual(old_data['github'], new_data['github'])
        old_data.pop('github'), new_data.pop('github')
        self.assertEqual(old_data, new_data)


    def test_user_update_valid_bio_from_post(self):
        password = 'P455w0rd123!'
        user = self.helper_functions.create_user(password=password)
        old_data = UserSerializer(user).data
        url = reverse('edit_user')
        self.client.login(username=user.username, password=password)

        new_bio = 'This is a bio!!!!$#zw4xe5cr6vt7by8nu9im'
        data = {'bio':new_bio}
        with transaction.atomic():
            response = self.client.post(url, data=data)

        updated_user = User.objects.get(username=user.username)
        new_data = UserSerializer(updated_user).data

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertNotEqual(old_data['bio'], new_data['bio'])
        old_data.pop('bio'), new_data.pop('bio')
        self.assertEqual(old_data, new_data)
