from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from service.models.author import Author
from service.models.post import Post
from service.models.likes import Likes
from service.serializers.likes import LikesSerializer
import json


class LikedTests(TestCase):

    def setUp(self):
        self.user1_password = "12345"
        self.user1 = User.objects.create_user("joeguy", "joeguy@email.com", self.user1_password)

        self.author1 = Author.objects.create(displayName = "Joe Guy", host = "http://localhost:8000", user = self.user1)

        self.post1 = Post.objects.create(title="Hello World!", author=self.author1)
        self.post2 = Post.objects.create(title="Test222", author=self.author1)
        
        self.likes1 = Likes.objects.create(context="Test", summary="Testing Now", author=self.author1, object=str(self.post1._id))
        self.likes2 = Likes.objects.create(context="Test222", summary="Testing Now22", author=self.author1, object=str(self.post2._id))

        self.client = APIClient()
    

    def tearDown(self):
        self.user1.delete()
        self.author1.delete()
        self.post1.delete()
        self.post2.delete()
        self.likes1.delete()
        self.likes2.delete()


    def test_liked(self):
        path = f"/service/authors/{self.author1._id}/liked/"
        response = self.client.generic(method="GET", path=path)

        print(json.dumps(response.data))

        self.assertEqual(json.dumps(LikesSerializer(self.likes1).data), json.dumps(response.data["liked"]["items"][0]))
        self.assertEqual(json.dumps(LikesSerializer(self.likes2).data), json.dumps(response.data["liked"]["items"][1]))