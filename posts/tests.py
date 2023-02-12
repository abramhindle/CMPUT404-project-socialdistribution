from django.test import TestCase
from .models import Post

class ModelTesting(TestCase):

    def setUp(self):
        self.post = Post.objects.create(
                type = "post",
                title = "example post",
                post_id = "http://127.0.0.1:5454/authors/1/posts/1",
                post_source = "http://lastplaceigotthisfrom.com/posts/yyyyy",
                post_origin = "http://whereitcamefrom.com/posts/zzzzz",
                description = "this is an example post for testing",
                content_type = "text/plain",
                content = "testing... 1,2,3",
                comment_count = 0,
                comments = "http://127.0.0.1:5454/authors/1/posts/1/comments",
                pub_date = "2015-03-09T13:07:04+00:00",
                is_unlisted = False
                )

    def test_post_model_is_valid(self):
        d = self.post
        self.assertTrue(isinstance(d, Post))

    def test_post_model_str(self):
        d = self.post
        self.assertEqual(str(d), "example post")
