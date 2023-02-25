from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from service.models.author import Author
from service.models.post import Post
from service.models.likes import Likes
from service.serializers.likes import LikesSerializer
import json

class LikesTests(TestCase):

    def setUp(self):
        self.user1_password = "12345"
        self.user1 = User.objects.create_user("joeguy", "joeguy@email.com", self.user1_password)
        self.user2_password = "1234"
        self.user2 = User.objects.create_user("somebody", "somebody@email.com", self.user2_password)

        self.author1 = Author.objects.create(displayName = "Joe Guy", host = "http://localhost:8000", user = self.user1)
        self.author2 = Author.objects.create(displayName = "Somebody Else", host = "http://localhost:8000", user = self.user2)

        self.post1 = Post.objects.create(title="Hello World!", author=self.author1)

        self.likes1 = Likes.objects.create(context="Test", summary="Testing Now", author=self.author1, object=str(self.post1._id))
        self.likes2 = Likes.objects.create(context="Test222", summary="Testing Now", author=self.author2, object=str(self.post1._id))

        self.client = APIClient()
    
    def tearDown(self):
        self.user1.delete()
        self.user2.delete()
        self.author1.delete()
        self.author2.delete()
        self.post1.delete()
        self.likes1.delete()
        self.likes2.delete()


    def test_post_likes(self):
        path = "/service/authors/{}/posts/{}/likes/".format(self.author1._id, self.post1._id)
        response = self.client.generic(method="GET", path=path)

        self.assertEqual(json.dumps(LikesSerializer(self.likes1).data), json.dumps(response.data["likes"][0]))
        self.assertEqual(json.dumps(LikesSerializer(self.likes2).data), json.dumps(response.data["likes"][1]))


    # #need to be implemented when comment modesl implemented
    # def test_comment_likes(self):
    #     path = "/service/authors/{}/posts/{}/comments/{}/likes/".format(self.author1._id, self.post1._id, self.comment1._id)
    #     response = self.client.generic(method="GET", path=path)

    #     self.assertEqual(self.likes1.toJSON(), response.data["likes"][0])     