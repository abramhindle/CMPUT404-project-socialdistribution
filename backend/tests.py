from django.test import TestCase, Client
import rest_framework
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from .models import *
from django.urls import reverse
import uuid

# Create your tests here.
# {"type":"author","id":"http://localhost:8000/author/f19f85f5605f4aed86376ced9fede5d9","host":"localhost:8000","displayName":"Tom van Maren","url":"http://localhost:8000/author/f19f85f5605f4aed86376ced9fede5d9","github":"https://github.com/"}


# class AuthorViewSetTestCase(APITestCase):

#     def setUp(self):
#         self.client = Client(HTTP_HOST='127.0.0.1:8000',
#                              ALLOWED_HOSTS='127.0.0.1')
#         response = self.client.post('/api/auth/register', {"displayName": "Test User",
#                                                            "github": "https://github.com/", "password": "test1234", "username": "testuser"}, format='json')
#         print(response.context)
#         self.author_id = response.context["id"].split("/")[-1]
#         return super().setUp()

#     def test_get_author(self):
#         response = self.client.get('author/' + self.author_id)
#         print(response)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.content["displayName"], "Test User")
# CREATED_AUTHOR =
#self.assertEqual(Author.objects.filter(token=response.id.split("/")[-1]).get().displayName, "Test User")


# class PostTest(APITestCase):
#    	def

class AuthorTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username='testDude', password='testpassword')
        self.testUser = Author.objects.create(id=str(
            uuid.uuid4()), user=user, displayName="TestDude")
        self.testUser.save()

    def test_display_name(self):
        # tests that when a user sets their display name it doesnt default back to the username
        user = Author.objects.get(displayName="TestDude")
        self.assertEqual(user.displayName, "TestDude")

    # def test_response_code(self):
    #     # Tests reponse codes returned by creation of a author

    def tearDown(self):
        self.testUser.delete()
