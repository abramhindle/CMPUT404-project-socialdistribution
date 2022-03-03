from django.forms import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model
from posts.models import Post, Comment

from .constants import COMMENT_DATA, POST_DATA

CURRENT_USER = 'bob'


class PostTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(username=CURRENT_USER, password='password')

    def test_create_post(self):
        post = Post.objects.create(
            title=POST_DATA['title'],
            description=POST_DATA['description'],
            content_type=POST_DATA['content_type'],
            content=POST_DATA['content'],
            author_id=get_user_model().objects.get(username=CURRENT_USER).id,
            unlisted=POST_DATA['unlisted'])
        post.full_clean()
        post.save()
        self.assertEqual(Post.objects.get(id=post.id), post)

    def test_invalid_content_type(self):
        post = Post.objects.create(
            title=POST_DATA['title'],
            description=POST_DATA['description'],
            content_type='some-obscure-content-type',
            content=POST_DATA['content'],
            author_id=get_user_model().objects.get(username=CURRENT_USER).id,
            unlisted=POST_DATA['unlisted'])
        with self.assertRaises(ValidationError):
            post.full_clean()

    def test_categories_association(self):
        post = Post.objects.create(
            title=POST_DATA['title'],
            description=POST_DATA['description'],
            content_type=POST_DATA['content_type'],
            content=POST_DATA['content'],
            author_id=get_user_model().objects.get(username=CURRENT_USER).id,
            unlisted=POST_DATA['unlisted'])
        post.full_clean()

        post.categories.create(category='web')
        post.categories.create(category='tutorial')
        post.save()

        self.assertEqual(2, len(post.categories.all()))


class CommentTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username=CURRENT_USER, password='password')
        self.post = Post.objects.create(
            title=POST_DATA['title'],
            description=POST_DATA['description'],
            content_type=POST_DATA['content_type'],
            content=POST_DATA['content'],
            author_id=get_user_model().objects.get(username=CURRENT_USER).id,
            unlisted=POST_DATA['unlisted'])

    def test_post_association(self):
        Comment.objects.create(
            comment=COMMENT_DATA['comment'],
            author_id=self.post.id,
            post_id=self.post.id,
            content_type=COMMENT_DATA['content_type'],
        )
        self.assertEqual(len(self.post.comment_set.all()), 1)
