from django.test import TestCase, Client
from post.models import Comment, Like, Post
from author.views import *
# Create your tests here.
class TestPostViewsComments(TestCase):

    def setUp(self):
        self.AUTHOR_ID = "a10d1b3c-5dae-451b-86bd-900a3f609c15"
        self.POST_ID = "3ea43954-7ca4-4107-9e42-1a0f5fa09f15"
        Author.objects.create(
            authorID=self.AUTHOR_ID,
            displayName="author1",
            host="http://ualberta.ca/"
        )
        Post.objects.create(
            postID = self.POST_ID,
            ownerID = self.AUTHOR_ID,
            date = timezone.now(),
            title = "test post",
            content = "text content",
            source = None,
            origin = None,
            description = "test description",
            categories = "wicked;cool",
            isPublic = True,
            isListed = True,
            hasImage = False,
            contentType = "text/markdown"
        )
        self.VIEW_URL = "/service/posts/" + self.POST_ID + "/comments"


    def testGetComments(self):
        pass

    def testPostComment(self):
        pass