from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from service.models.author import Author
from service.models.post import Post
from service.models.likes import Likes
from service.models.liked import Liked
from service.serializers.liked import LikedSerializer
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
        self.likes = [self.likes1, self.likes2]

        self.liked1 = Liked.objects.create()
        self.liked1.items.set(self.likes)

        self.client = APIClient()
    

    def tearDown(self):
        self.user1.delete()
        self.author1.delete()
        self.post1.delete()
        self.post2.delete()
        self.likes1.delete()
        self.likes2.delete()
        self.liked1.delete()


    def test_liked(self):
        path = f"/service/authors/{self.author1._id}/liked/"
        response = self.client.generic(method="GET", path=path)

        self.assertJSONEqual(json.dumps(LikedSerializer(self.liked1).data), json.loads(response.data["liked"]))