import json
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from posts.models import Post, ContentType

from posts.tests.constants import POST_DATA
from .constants import POST_IMG_DATA

TEST_USERNAME = 'bob'
TEST_PASSWORD = 'password'


class AuthorTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        get_user_model().objects.create_user(username=TEST_USERNAME, password=TEST_PASSWORD)

    def test_authors(self):
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        res = self.client.get('/api/v1/authors/')
        self.assertEqual(res.status_code, 200)
        body = json.loads(res.content.decode('utf-8'))
        self.assertEqual(body['type'], 'authors')
        self.assertEqual(len(body['items']), 1)

    def test_authors_require_login(self):
        res = self.client.get('/api/v1/authors/')
        self.assertEqual(res.status_code, 403)

    def test_create_author(self):
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        res = self.client.post('/api/v1/authors/', {'username': 'alice', 'password': 'some_password'})
        self.assertEqual(res.status_code, 405)

    def test_allow_api_users(self):
        api_user_username = 'api_user'
        api_user = get_user_model().objects.create_user(username=api_user_username, password=TEST_PASSWORD)
        api_user.is_api_user = True
        api_user.save()

        self.client.login(username=api_user_username, password=TEST_PASSWORD)
        res = self.client.get('/api/v1/authors/')
        self.assertEqual(res.status_code, 200)


class PostTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='bob', password='password')
        self.post = Post.objects.create(
            title=POST_DATA['title'],
            description=POST_DATA['description'],
            content_type=POST_DATA['content_type'],
            content=POST_DATA['content'],
            author_id=self.user.id,
            unlisted=POST_DATA['unlisted'])

        self.other_user = get_user_model().objects.create_user(username='alice', password='password')
        self.post_by_other_user = Post.objects.create(
            title=POST_DATA['title'],
            description=POST_DATA['description'],
            content_type=POST_DATA['content_type'],
            content=POST_DATA['content'],
            author_id=self.other_user.id,
            unlisted=POST_DATA['unlisted'])
        self.post_by_other_user.save()

    def test_posts(self):
        self.client.login(username='bob', password='password')
        res = self.client.get(f'/api/v1/authors/{self.user.id}/posts/')
        self.assertEqual(res.status_code, 200)
        body = json.loads(res.content.decode('utf-8'))
        self.assertEqual(body['type'], 'posts')
        self.assertEqual(len(body['items']), 1)

        for post in body['items']:
            self.assertIn('id', post)
            self.assertIn('title', post)
            self.assertIn('content', post)
            self.assertIn('author', post)
            self.assertIn('visibility', post)
            self.assertIn('unlisted', post)
            self.assertIn('type', post)
            self.assertIn('contentType', post)
            self.assertIn('published', post)
            self.assertIn('url', post)
            self.assertIn('categories', post)

    def test_posts_require_login(self):
        res = self.client.get(f'/api/v1/authors/{self.user.id}/posts/')
        self.assertEqual(res.status_code, 403)

    def test_post_detail(self):
        self.client.login(username='bob', password='password')
        res = self.client.get(f'/api/v1/authors/{self.user.id}/posts/{self.post.id}/')
        self.assertEqual(res.status_code, 200)
        post = json.loads(res.content.decode('utf-8'))

        self.assertIn('id', post)
        self.assertIn('title', post)
        self.assertIn('content', post)
        self.assertIn('author', post)
        self.assertIn('visibility', post)
        self.assertIn('unlisted', post)
        self.assertIn('type', post)
        self.assertIn('contentType', post)
        self.assertIn('published', post)
        self.assertIn('url', post)
        self.assertIn('categories', post)


class ImageTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.author = get_user_model().objects.create_user(username='bob', password='password')

        self.post = Post.objects.create(
            title=POST_DATA['title'],
            description=POST_DATA['description'],
            content_type=POST_DATA['content_type'],
            content=POST_DATA['content'],
            author_id=self.author.id,
            unlisted=POST_DATA['unlisted'])
        self.post.full_clean()
        self.post.save()

        self.img_post = Post.objects.create(
            title=POST_IMG_DATA['title'],
            description=POST_IMG_DATA['description'],
            content_type=POST_IMG_DATA['content_type'],
            content=POST_IMG_DATA['content'],
            img_content=POST_IMG_DATA['img_content'],
            author_id=self.author.id,
            unlisted=POST_IMG_DATA['unlisted'])
        self.img_post.full_clean()
        self.img_post.save()

        return

    def test_image(self):
        self.client.login(username='bob', password='password')
        res2 = self.client.get(f'/api/v1/authors/{self.author.id}/posts/{self.img_post.id}/image/')
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(res2.headers['Content-Type'], ContentType.PNG)

    def test_not_image_404(self):
        self.client.login(username='bob', password='password')
        res = self.client.get(f'/api/v1/authors/{self.author.id}/posts/{self.post.id}/image/')
        self.assertEqual(res.status_code, 404)

    def test_image_require_login(self):
        res = self.client.get(f'/api/v1/authors/{self.author.id}/posts/{self.img_post.id}/image/')
        self.assertEqual(res.status_code, 403)
