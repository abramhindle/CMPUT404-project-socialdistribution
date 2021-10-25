from django.test import TestCase
from mixer.backend.django import mixer
from datetime import timedelta
from .models import *
from .builders import *


class PostTest(TestCase):
    def test_post_is_public(self):
        visibility = Post.FRIENDS
        post = PostBuilder().visibility(visibility).build()
        self.assertFalse(post.is_public())

    def test_post_when(self):
        time = datetime.now(timezone.utc)
        post = PostBuilder().pub_date(time).build()
        self.assertTrue(post.when() == 'just now')

    def test_post_total_likes(self):
        likes = 25
        post = PostBuilder().likes(likes).build()
        self.assertTrue(post.total_likes() == likes)


class CommentModelTests(TestCase):

    def test_when_just_now (self):
        '''
            comment.when() returns just now right after post creation
        '''
        author = mixer.blend(Author)
        post = mixer.blend(Post, author = author)
        comment = mixer.blend(Comment, author=author, post=post, pub_date = datetime.now(timezone.utc) )

        self.assertIs( comment.when() == 'just now', True)

    def test_when_10_seconds (self):
        '''
            comment.when() returns 10 seconds ago after the time has passed
        '''
        author = mixer.blend(Author)
        post = mixer.blend(Post, author = author)

        pub_date = datetime.now(timezone.utc) - timedelta(seconds=10)
        comment = mixer.blend(Comment, author=author, post=post, pub_date = pub_date  )

        self.assertIs( comment.when() == '10 seconds ago', True)