from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from service.models.author import Author
from service.models.post import Post
from service.models.comment import Comment
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

        self.comment1 = Comment.objects.create(comment="This is a comment.", author=self.author1, post=self.post1)

        self.client = APIClient()

    
    def tearDown(self):
        self.user1.delete()
        self.user2.delete()
        self.author1.delete()
        self.author2.delete()
        self.post1.delete()
        self.comment1.delete()


    def test_post_likes(self):
        pass
