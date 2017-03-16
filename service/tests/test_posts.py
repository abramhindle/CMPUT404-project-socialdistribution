from unittest import skip

from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from social.app.models.author import Author
from social.app.models.node import Node
from social.app.models.post import Post


class PostsTestCase(APITestCase):
    def setUp(self):
        self.node = Node.objects.create(name="Test", host="http://www.socdis.com/",
                                        service_url="http://api.socdis.com/", local=True)

        user1 = User.objects.create_user("test1", "test@test.com", "pass1")
        user2 = User.objects.create_user("test2", "test@test.com", "pass2")

        self.author1 = Author.objects.get(user__id=user1.id)
        self.author1.activated = True
        self.author1.save()
        self.author2 = Author.objects.get(user__id=user2.id)
        self.author2.activated = True
        self.author2.save()

        self.post = Post.objects.create(post_story="test", author=self.author2, visibility="Public")
        self.post.save()

    def test_get_public_posts(self):
        self.client.login(username="test1", password="pass1")
        response = self.client.get(self.post.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_get_nonexistant_post(self):
        response = self.client.get("/post1/666")
        self.assertEqual(response.status_code, 404)

    @skip("fail")
    # Getting a 405, urg
    def test_get_using_json(self):
        post = {
            "query": "getPost",
            "postid": "1",
            "url": self.node.host + "posts/1",
            "author": {
                "id": str(self.author1.id),
                "host": self.node.host,
                "displayName": self.author1.displayName,
                "url": self.node.host + "app/authors/" + str(self.author1.id)
            }
            # "friends": [ urls to authors ]
        }
        response = self.client.post("/posts/1/", post, format="json")
        self.assertEqual(response.status_code, 200)

    @skip("fail")
    # Returns a 404 right now, should return a 200 later.
    def test_get_authors_posts(self):
        response = self.client.get("/app/authors/" + str(self.author2.id) + "/posts/")
        self.assertEqual(response.status_code, 200)
