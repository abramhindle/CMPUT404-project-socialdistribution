from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from social.app.models.author import Author
from social.app.models.comment import Comment
from social.app.models.node import Node
from social.app.models.post import Post


class CommentModelTests(TestCase):
    def setUp(self):
        self.node = Node.objects.create(name="Test", host="http://www.socdis.com/",
                                        service_url="http://api.socdis.com/", local=True)

        user1 = User.objects.create_user("test1", "test@test.com", "pass1")
        self.author1 = Author.objects.get(user__id=user1.id)
        self.post = Post.objects.create(post_story="test", author=self.author1, visibility="Public")
        self.comment = Comment.objects.create(text="text", post_id=self.post.id, author_id=self.author1.id)

    # There's not much to test here.
    def test_non_empty_time(self):
        self.assertIsNotNone(self.comment.created)

    def test_comment_str(self):
        self.assertEquals(str(self.comment),
                          "Comment by " + str(self.author1) + " on " + str(self.post) + ": " + self.comment.text)
