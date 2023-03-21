from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from service.models.author import Author
import json

class AuthTests(TestCase):

    def setUp(self):
        self.user1_password = "12345"
        self.user1 = User.objects.create_user("joeguy", "joeguy@email.com", self.user1_password)
        self.user2_password = "1234"
        self.user2 = User.objects.create_user("somebody", "somebody@email.com", self.user2_password)

        self.author1 = Author.objects.create(displayName = "Joe Guy", host = "http://localhost:8000", user = self.user1)
        self.client = APIClient()

    
    def tearDown(self):
        self.user1.delete()
        self.user2.delete()
        self.author1.delete()

    
    def test_signIn_author(self):
        body = {
            "username": self.user1.username,
            "password": self.user1_password
        }
        response = self.client.generic(method="POST", path="/api/signin/", data=json.dumps(body), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["author"], self.author1.toJSON())


    def test_signOut(self):
        response = self.client.post("/api/signout/")
        self.assertEqual(response.status_code, 200)


    def test_signIn_non_author(self):
        body = {
            "username": self.user2.username,
            "password": self.user2_password
        }
        response = self.client.post("/api/signin/", json.dumps(body), format="json")
        self.assertEqual(response.status_code, 401)
        

    def test_signIn_wrong_info(self):
        body = {
            "username": self.user2.username,
            "password": self.user1_password
        }
        self.assertNotEqual(self.user1_password, self.user2_password)
        response = self.client.post("/api/signin/", json.dumps(body), format="json")
        self.assertEqual(response.status_code, 401)