from django.test import TestCase
from .models import *
from .builders import *

# Create your tests here.
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