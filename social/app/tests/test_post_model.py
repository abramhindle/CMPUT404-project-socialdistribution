from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from social.app.models.author import Author
from social.app.models.node import Node
from social.app.models.post import Post


class PostModelTests(TestCase):
    def setUp(self):
        self.node = Node.objects.create(name="Test", host="http://www.socdis.com/",
                                        service_url="http://api.socdis.com/", local=True)

        user1 = User.objects.create_user("test1", "test@test.com", "pass1")
        self.author1 = Author.objects.get(user__id=user1.id)
        self.post = Post.objects.create(post_story="test", author=self.author1, visibility="Public")

    def test_correct_url(self):
        self.assertEquals(self.post.get_absolute_url(), "/posts/1/")

    def test_getting_posts_str(self):
        self.assertEquals(self.post.__str__(), "test")

    def test_generated_time(self):
        self.assertIsNotNone(self.post.pub_date)
        self.assertIsNotNone(self.post.last_modified)

    def test_visibility(self):
        self.assertEquals(self.post.visibility, "Public")
        self.post.visibility = "FOAF"
        self.assertEquals(self.post.visibility, "FOAF")
        self.post.visibility = "Friends"
        self.assertEquals(self.post.visibility, "Friends")
        self.post.visibility = "Private"
        self.assertEquals(self.post.visibility, "Private")
        self.post.visibility = "SERVERONLY"
        self.assertEquals(self.post.visibility, "SERVERONLY")
