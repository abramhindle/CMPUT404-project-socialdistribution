from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from service.models.author import Author
from service.models.post import Post
from service.models.comment import Comment
from django.test import *
from service.models.author import Author
from django.contrib.auth.models import User
from service.views.author import *
from service.views.follower import *
from service.views.liked import *
import json

from django.urls import reverse

class LikesTests(TestCase):

    def setUp(self):

        self.liked_view = LikedView()
        self.likes_view = LikesView()

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


    def test_get_author_likes_empty(self):

        request = HttpRequest()
        request.method = "get"

        get_response = self.liked_view.get(request, self.author1._id)
        self.assertEqual(get_response.status_code, 200)
        content = get_response.data

        self.assertEqual(content["items"], [])

    def test_get_author_likes(self):

        request = HttpRequest()
        request.method = "get"

        like = Like()
        like.author=self.author2
        like.object=self.post1._id
        like.save()

        get_response = self.liked_view.get(request, self.author2._id)
        self.assertEqual(get_response.status_code, 200)
        content = get_response.data

        self.assertEqual(content["items"][0], like.toJSON())

    def test_get_post_likes(self):
        request = HttpRequest()
        request.method = "get"

        like = Like()
        like.author=self.author2
        like.object=self.post1._id
        like.save()

        get_response = self.likes_view.get(request, self.author1._id, self.post1._id) #this one gets from a post
        self.assertEqual(get_response.status_code, 200)
        content = get_response.data

        self.assertEqual(content["items"][0], like.toJSON())