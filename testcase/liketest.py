from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from myapp.models import Post, Comment, Author

class LikeTests(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            display_name="John Doe",
            host="http://127.0.0.1:8000/",
            github="http://github.com/johndoe",
            url="http://127.0.0.1:8000/authors/johndoe",
            profile_image="https://i.imgur.com/5hFv5yL.jpeg"
        )
        self.post = Post.objects.create(
            title="Test Post",
            content="This is a test post.",
            author=self.author
        )
        self.comment = Comment.objects.create(
            post=self.post,
            content="This is a test comment.",
            author=self.author
        )

    def test_like_post(self):
        client = APIClient()
        url = reverse("author-post-likes", args=[self.author.id, self.post.id])
        data = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "John Doe likes your post",
            "type": "Like",
            "author": {
                "type": "author",
                "id": self.author.url,
                "host": self.author.host,
                "displayName": self.author.display_name,
                "url": self.author.url,
                "github": self.author.github,
                "profileImage": self.author.profile_image
            },
            "object": self.post.url
        }
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_like_comment(self):
        client = APIClient()
        url = reverse("author-comment-likes", args=[self.author.id, self.post.id, self.comment.id])
        data = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "John Doe likes your comment",
            "type": "Like",
            "author": {
                "type": "author",
                "id": self.author.url,
                "host": self.author.host,
                "displayName": self.author.display_name,
                "url": self.author.url,
                "github": self.author.github,
                "profileImage": self.author.profile_image
            },
            "object": self.comment.url
        }
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_post_likes(self):
        client = APIClient()
        url = reverse("author-post-likes", args=[self.author.id, self.post.id])
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["items"]), 1)
        self.assertEqual(response.data["items"][0]["object"], self.post.url)

    def test_get_comment_likes(self):
        client = APIClient()
        url = reverse("author-comment-likes", args=[self.author.id, self.post.id, self.comment.id])
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["items"]), 1)
        self.assertEqual(response.data["items"][0]["object"], self.comment.url)

    def test_get_liked_objects(self):
        client = APIClient()
        url = reverse("author-liked", args=[self.author.id])
        response =
