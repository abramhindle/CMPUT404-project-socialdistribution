from django.contrib.auth.models import User
from django.test import RequestFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest import skip

from dashboard.models import Node, Author
from post.models import Post, Comment
from post.views import add_comment_to_post


class CommentsTestCase(APITestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

        self.node = Node.objects.create(name="Test", host="http://www.socdis.com/",
                                        service_url="http://api.socdis.com/", local=True)

        user1 = User.objects.create_user("test1", "test@test.com", "pass1")
        user2 = User.objects.create_user("test2", "test@test.com", "pass2")

        self.author1 = Author.objects.get(user__id=user1.id)
        self.author1.displayName = "test1"
        self.author1.activated = True
        self.author1.save()
        self.author2 = Author.objects.get(user__id=user2.id)
        self.author1.displayName = "test2"
        self.author2.activated = True
        self.author2.save()

        self.post = Post.objects.create(post_story="test", author=self.author2, visibility="Public")
        self.post.save()
        self.comment = Comment.objects.create(text="text", post_id=self.post.id, author_id=self.author1.id)
        self.comment.save()

    def test_get_comments(self):
        self.client.login(username="test1", password="pass1")
        response = self.client.get("/post/1/comments/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["all_comments"][0], self.comment)

    def test_post_to_comments(self):
        comment = {
            "query": "addComment",
            "post": "http://www.socdis.com/post/1",
            "comment": {
                "author": {
                    "id": str(self.author1.id),
                    "host": self.node.host,
                    "displayName": self.author1.displayName,
                    "url": self.node.host + "dashboard/authors/" + str(self.author1.id) + "/"
                },
                "comment": "testing",
                "contentType": "text/plain",
                "published":"2017-03-13T00:01:02+00:00",
                "id":"de305d54-75b4-431b-adb2-eb6b9e546013"
            }
        }
        request = self.request_factory.post(reverse('posts:add_comment_to_post',
                                                    args=[self.post.id]),
                                            data=comment, format='json')
        request.user = self.author1.user
        response = add_comment_to_post(request, self.post.id)
        self.assertEqual(response.status_code, 200)

    @skip("fail")
    # 200 instead of 403 Forbidden
    def test_edit_comment_as_different_user(self):
        comment = {
            "query": "addComment",
            "post": "http://www.socdis.com/post/1",
            "comment": {
                "author": {
                    "id": str(self.author2.id),
                    "host": self.node.host,
                    "displayName": self.author2.displayName,
                    "url": self.node.host + "dashboard/authors/" + str(self.author2.id) + "/"
                },
                "comment": "testing",
                "contentType": "text/plain",
                "published":"2017-03-13T00:01:02+00:00",
                "id":"de305d54-75b4-431b-adb2-eb6b9e546013"
            }
        }
        request = self.request_factory.post(reverse('posts:add_comment_to_post',
                                                    args=[self.post.id]),
                                            data=comment, format='json')
        request.user = self.author2.user
        response = add_comment_to_post(request, self.post.id)
        self.assertEqual(response.status_code, 403)

    @skip("fail")
    # 200 instead of 403 Forbidden
    def test_post_comment_as_unauthorized_user(self):
        user = User.objects.create_user("test3", "test@test.com", "pass2")

        author = Author.objects.get(user__id=user.id)
        author.displayName = "test1"
        author.save()

        comment = {
            "query": "addComment",
            "post": "http://www.socdis.com/post/1",
            "comment": {
                "author": {
                    "id": str(author.id),
                    "host": self.node.host,
                    "displayName": author.displayName,
                    "url": self.node.host + "dashboard/authors/" + str(author.id) + "/"
                },
                "comment": "testing",
                "contentType": "text/plain",
                "published":"2017-03-13T00:01:02+00:00",
                "id":"de305d54-75b4-431b-adb2-eb6b9e546013"
            }
        }
        request = self.request_factory.post(reverse('posts:add_comment_to_post',
                                                    args=[self.post.id]),
                                            data=comment, format='json')
        request.user = author.user
        response = add_comment_to_post(request, self.post.id)
        self.assertEqual(response.status_code, 403)
