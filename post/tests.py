from django.test import TestCase, Client
from post.models import Comment, Like, Post
from author.views import *
# Create your tests here.
class TestPostViewsComments(TestCase):

    def setUp(self):
        self.AUTHOR_ID = "a10d1b3c-5dae-451b-86bd-900a3f609c15"
        self.USERNAME = "new_username"
        self.PASSWORD = "new_password"
        self.USER = User.objects.create_user(username=self.USERNAME, password=self.PASSWORD)
        self.DISPLAY_NAME = "author1"
        self.HOST = "http://ualberta.ca/"
        self.POST_ID = "3ea43954-7ca4-4107-9e42-1a0f5fa09f15"
        self.AUTHOR = Author.objects.create(
            user = self.USER,
            authorID=self.AUTHOR_ID,
            displayName=self.DISPLAY_NAME,
            host=self.HOST
        )
        self.POST = Post.objects.create(
            postID = self.POST_ID,
            ownerID = self.AUTHOR,
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
        self.VIEW_URL = "/service/author/" + self.AUTHOR_ID + "/posts/" + self.POST_ID + "/comments"

    def testGetComments(self):
        Comment.objects.create(
            commentID = "72b207f8-5c7b-4a46-a39d-c9085d218a89",
            postID = self.POST,
            authorID = self.AUTHOR,
            date = timezone.now(),
            content = "Some interesting comment.",
            contentType = "text"
        )
        Comment.objects.create(
            commentID = "af0a5c34-49c9-4314-92f3-88b07f43fab7",
            postID = self.POST,
            authorID = self.AUTHOR,
            date = timezone.now(),
            content = "<h1>Some interesting comment.</h1>",
            contentType = "markdown"
        )

        c = Client()
        c.force_login(self.USER)
        response = c.get(self.VIEW_URL)
        print(response)
        content = response.json()
        self.assertEqual(2, len(content["comments"]))
        self.assertEqual(response.status_code, 200)

    def testPostComment(self):
        post_data = {
            "type": "comment",
            "author": {
                "type": "author",
                "id": self.HOST + "author/" + self.AUTHOR_ID,
                "url": self.HOST + "author/" + self.AUTHOR_ID,
                "host": self.HOST,
                "displayName": self.DISPLAY_NAME,
                "github": None,
                "profileImage": None
            },
            "comment": "A very insightful comment.",
            "contentType": "text/markdown",
            "id": self.HOST + "author/" + self.AUTHOR_ID + "/comments/" + "a111da12-d7ca-4527-858c-80691bb51061",
            "published": "2021-03-09T13:07:04+00:00"
        }

        c = Client()
        c.force_login(self.USER)
        response = c.post(self.VIEW_URL, post_data, "application/json")
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, Comment.objects.count())