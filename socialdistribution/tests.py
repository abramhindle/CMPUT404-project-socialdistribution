import json
from unittest.mock import MagicMock, patch
from requests import Response
from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from api.tests.constants import SAMPLE_REMOTE_POST
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
        mock_json_response = json.loads(SAMPLE_REMOTE_POST)
        mock_response = Response()
        mock_response.url = 'http://localhost:5555/api/v2/authors/1/posts'
        mock_response.json = MagicMock(return_value=mock_json_response)

        mock_server = Server(
            service_address="http://localhost:5555/api/v2",
            username="hello",
            password="no",
        )
        mock_server.get = MagicMock(return_value=mock_response)

        with patch.object(StreamView, 'get_server_to_endpoints_mapping') as mock_get_server_to_endpoints_mapping:
            mock_server_to_endpoints_mapping = [(mock_server, ['/authors/1/posts'])]
            mock_get_server_to_endpoints_mapping.return_value = mock_server_to_endpoints_mapping
            with patch('servers.models.Server.objects') as MockServerObjects:
                MockServerObjects.all.return_value = [mock_server]

                self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
                res = self.client.get(reverse_lazy('stream'))
                self.assertEqual(res.status_code, 200)

                self.assertContains(res, mock_json_response[0]['title'])
