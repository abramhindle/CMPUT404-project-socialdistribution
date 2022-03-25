import json
from unittest.mock import MagicMock
from requests import Response
from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from api.tests.test_api import TEST_PASSWORD, TEST_USERNAME

from posts.models import Post
from posts.tests.constants import POST_DATA
from servers.models import Server
from socialdistribution.views import StreamView


class ViewsTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_redirect(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.get('Location'), reverse_lazy('auth_provider:login'))


class StreamViewTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(username=TEST_USERNAME, password=TEST_PASSWORD)
        self.num_posts = 10
        for i in range(self.num_posts):
            post = Post.objects.create(
                title=POST_DATA['title'],
                description=POST_DATA['description'],
                content_type=POST_DATA['content_type'],
                content=POST_DATA['content'],
                author_id=self.user.id,
                unlisted=POST_DATA['unlisted'])
            post.save()

    def test_uses_the_correct_template(self):
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        res = self.client.get(reverse_lazy('stream'))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'stream.html')

    def test_displays_our_posts(self):
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        res = self.client.get(reverse_lazy('stream'))
        self.assertEqual(res.status_code, 200)

        self.assertContains(res, POST_DATA['title'], count=self.num_posts)

    def test_displays_remote_posts(self):
        # TODO: Update this when our groupmates have updated their interface
        mock_raw_json_response = '''[
            {
                "title": "anonymouspost",
                "id": "1",
                "source": "https://cmput404-project-t12.herokuapp.com/posts/1",
                "origin": "https://cmput404-project-t12.herokuapp.com/posts/1",
                "description": "anonymouspost",
                "contentType": "text",
                "content": "anonymouspost",
                "image": null,
                "image_src": "",
                "author": "3",
                "categories": "undefined",
                "like_count": 3,
                "comments": "",
                "published": "2022-03-21T22:44:16.876579Z",
                "visibility": "PUBLIC",
                "unlisted": false
            }
        ]'''
        mock_json_response = json.loads(mock_raw_json_response)
        mock_response = Response()
        mock_response.url = 'http://localhost:5555/api/v2/authors/1/posts'
        mock_response.json = MagicMock(return_value=mock_json_response)

        mock_server = Server(
            service_address="http://localhost:5555/api/v2",
            username="hello",
            password="no",
        )
        mock_server.get = MagicMock(return_value=mock_response)

        mock_post_endpoints = [f'{mock_server.service_address}/authors/1/posts']
        StreamView.get_endpoints = MagicMock(return_value=mock_post_endpoints)

        mock_servers = [mock_server]
        Server.objects.all = MagicMock(return_value=mock_servers)

        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        res = self.client.get(reverse_lazy('stream'))
        self.assertEqual(res.status_code, 200)

        self.assertContains(res, mock_json_response[0]['title'])
