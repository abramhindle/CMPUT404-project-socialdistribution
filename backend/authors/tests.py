from django.urls import reverse
from rest_framework import status
from .serializers import AuthorSerializer
from rest_framework.test import APITestCase, force_authenticate
from django.contrib.auth.models import User
import json


def create_user(username):
    user = User.objects.create_user(username=username, password="test", email=f"{username}@gmail.com")
    user.is_superuser = True
    user.is_staff = True
    user.author.verified = True
    user.author.save()
    user.save()
    return user


class AccountTests(APITestCase):

    def setUp(self) -> None:
        create_user("SuperUser")

    def test_create_account(self):
        """ Ensure we can create a new account object. """
        user = User.objects.get(username='SuperUser')
        url = "/api/authors/register/"
        data = {'displayName': 'testUser', "password": "password", "github": "testUser"}
        response = self.client.post(url, data, format="json")
        force_authenticate(response, user=user)
        self.assertIn("id", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["type"], "author")
        self.assertEqual(response.data["url"], response.data["id"])
        self.assertEqual(response.data["host"], "http://127.0.0.1:8000/")
        self.assertEqual(response.data["displayName"], "testUser")
        self.assertEqual(response.data["github"], "https://www.github.com/testUser")
        self.assertEqual(response.data["profileImage"], f"{response.data['host']}api/authors/{response.data['id'].split('/')[-2]}/avatar/")

    def test_list_authors(self):
        """
        Ensure we can create a new account object.
        """
        # Create New Authors
        user_one = create_user("userOne")
        user_two = create_user("userTwo")

        # Fetch Authors
        url = f"/api/authors/"
        self.client.force_authenticate(user=User.objects.get(username='SuperUser'))
        response = self.client.get(url, format="json")
        data = json.loads(json.dumps(response.data))

        # Confirm Authors Are Returned
        self.assertEqual(len(data["items"]), 3)
        for user in [user_one, user_two]:
            self.assertIn(user.author.displayName, map(lambda x: x["displayName"], data["items"]))
            self.assertIn(user.author.id, map(lambda x: x["id"], data["items"]))
            self.assertIn(user.author.profileImage, map(lambda x: x["profileImage"], data["items"]))
