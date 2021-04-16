from backend.models import *

from django.urls import reverse

from rest_framework.test import APIClient, APITestCase
from rest_framework import status


USER_LOGIN_URL = reverse('author_login')


class TestAuthorViewSet(APITestCase):
    def setUp(self):
        test_user = User.objects.create_user(
            username='jon',
            password='youknownothing'
        )

        test_user2 = User.objects.create_user(
            username='arya',
            password='nonone'
        )

        self.client = APIClient()

        self.author_test = Author.objects.create(
            user=test_user,
            displayName='Jon Snow',
            host="http://localhost:8000/",
            github="https://www.github.com/johnSnow"
        )

        self.author_test2 = Author.objects.create(
            user=test_user2,
            displayName='Arya Stark',
            host="http://localhost:8000/",
            github="https://www.github.com/AryaStark"
        )

        self.author_test.save()
        self.author_test2.save()

    def test_login_author(self):
        """Testing for login of an author
        """
        test_login_data = {
            'username': 'jon',
            'password': 'youknownothing',
        }
        # Logging into author
        login_response = self.client.post(
            USER_LOGIN_URL, test_login_data, format='json')

        # checking for authorized user
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

    def test_incorrect_login_author(self):
        """Testing for an incorrect login of an author
        """
        incorrect_test_login_data = {
            'username': 'jon ',
            'password': 'muhqueen',
        }

        # Trying to Log into author
        login_response = self.client.post(
            USER_LOGIN_URL, incorrect_test_login_data, format='json')

        # checking for incorrect credentials
        self.assertEqual(login_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_auth_author(self):
        """Testing for login of an authorized author
        """
        # forcing authentication of an author
        self.client.force_authenticate(user=self.author_test.user)

        # getting an author
        author_response = self.client.get(
            reverse('author_object', kwargs={'id': self.author_test.id}))

        # checking for authorized user
        self.assertEqual(author_response.status_code, status.HTTP_200_OK)

    def test_retrieve_unauth_author(self):
        """Testing for unsuccessful login of an unauthorized author
        """

        # getting an author
        author_response = self.client.get(
            reverse('author_object', kwargs={'id': self.author_test.id}))

        # checking for authorized user
        self.assertEqual(author_response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

    def test_update_author(self):
        """Testing for an update (POST) of github url and displayName for author object created
        """
        # forcing authentication of an author
        self.client.force_authenticate(user=self.author_test.user)

        post_request = {
            "displayName": "Jon Targaryen",
            "github": "https://github.com/JonTarg2"
        }
        # getting an author
        update_response = self.client.post(
            reverse('author_object', kwargs={'id': self.author_test.id}),
            post_request,
            format='json'
        )

        # checking for authorized user
        self.assertEqual(update_response.status_code,
                         status.HTTP_200_OK)

        # checking for updated data for user
        self.assertEqual(update_response.data["displayName"], "Jon Targaryen")
        self.assertEqual(
            update_response.data["github"], "https://github.com/JonTarg2")

    def test_get_author_list(self):
        """Testing for an retrieving a list of all authors
        """
        # forcing authentication of an authors
        self.client.force_authenticate(user=self.author_test.user)
        self.client.force_authenticate(user=self.author_test2.user)

        # getting an author
        get_response = self.client.get(
            reverse('author_list'))

        # checking for OK status code
        self.assertEqual(get_response.status_code,
                         status.HTTP_200_OK)

        self.assertEqual(get_response.data[0]["displayName"], "Jon Snow")
        self.assertEqual(
            get_response.data[1]["displayName"], "Arya Stark")
        self.assertEqual(
            get_response.data[0]["type"], get_response.data[1]["type"])
