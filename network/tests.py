# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status

class AccountsTest(APITestCase):
    def setUp(self):
        # We want to go ahead and originally create a user. 
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        # URL for creating an account.
        self.create_url = reverse('account-create')

    def test_CreateUser(self):
        """
        Ensure that we can create a new user and that a valid token is created with it.
        """
        data = {
            'username': 'testuser1',
            'email': 'testuser1@example.com',
            'password': 'testuser1234'
        }
        response = self.client.post(self.create_url , data, format='json')
        
        # Checking to make sure that we have two users in the db.
        self.assertEqual(User.objects.count(), 2)
        # Checking that we return the correct status_code.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Checking the username and email
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertFalse('password' in response.data) 
    
    def test_CreateUser_shortPassword(self):
        """
        Ensure that the user is not created for password lengths less than 8.
        """
        data = {
                'username': 'testuser1',
                'email': 'testuser1@example.com',
                'password': 'test'
        }

        # Checking to make sure that we have one users in the db.
        self.assertEqual(User.objects.count(), 1)
        response = self.client.post(self.create_url, data, format='json')
        # Checking that we return the correct status_code.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Checking that password length is < 8
        self.assertEqual(len(response.data['password']), 1)

    def test_CreateUser_noPassword(self):
        data = {
                'username': 'testuser1',
                'email': 'testuser1@example.com',
                'password': ''
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)


    def test_CreateUser_longUsername(self):
        data = {
            'username': 'testuser1'*30,
            'email': 'testuser1@example.com',
            'password': 'testuser1234'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_CreateUser_noUsername(self):
        data = {
            'username': '',
            'email': 'testuser1@example.com',
            'password': 'testuser1234'
                }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_CreateUser_existingUsername(self):
        data = {
                'username': 'testuser',
                'email': 'user@example.com',
                'password': 'testuser'
                }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_CreateUser_with_existingEmail(self):
        data = {
            'username': 'testuser2',
            'email': 'test@example.com',
            'password': 'testuser'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_CreateUser_invalidEmail(self):
        data = {
            'username': 'testuser1',
            'email': 'testuser1',
            'password': 'testuser1234'
        }


        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_CreateUser_noEmail(self):
        data = {
                'username': 'testuser1',
                'email': '',
                'password': 'testuser1234'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)