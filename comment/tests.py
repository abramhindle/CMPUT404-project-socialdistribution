from django.test import TestCase
from django.test import Client
import uuid
from django.utils import unittest
from post.models import Post, VisibleToAuthor, PostImage
from django.contrib.auth.models import AnonymousUser, User
from django.test.utils import setup_test_environment
from django.test.client import Client
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from author.models import Author
from django.core.files import File
from comment.models import Comment


class CommentTestCase(TestCase):

    def setUp(self):
        setup_test_environment()
        user1 = User.objects.create_user(username="myuser1",
                                         password="mypassword")
        user2 = User.objects.create_user(username="myuser2",
                                         password="mypassword")

        author1 = Author.objects.create(user=user1, github_user='mygithubuser')
        author2 = Author.objects.create(user=user2, github_user='mygithubuser')

        post1 = Post.objects.create(
            author=author1,
            guid=uuid.uuid1(),
            title="title1",
            description="desc1",
            content="post1",
            visibility="PUBLIC")

        post2 = Post.objects.create(
            author=author1,
            guid=uuid.uuid1(),
            title="title2",
            description="desc2",
            content="post2",
            visibility="PUBLIC")
        post3 = Post.objects.create(
            author=author1,
            guid=uuid.uuid1(),
            title="title3",
            description="desc3",
            content="post3",
            visibility="PUBLIC")

        comment1=Comment.objects.create(
            author=author1,
            guid=uuid.uuid1(),
            post=post1,
            comment="comment1")

        comment2=Comment.objects.create(
            author=author1,            
            guid=uuid.uuid1(),
            post=post1,
            comment="comment2")

    def test_creating_comments(self):
        c = Client()
        response = c.post('/author/posts/create_post', {'title': '1', 'description': 'aaaa',
                                                        'text_body': '121',
                                                        'comments': 'comments'
                                                        })
        self.assertEqual(response.status_code, 301)

    def testGetSingleComment(self):
        'test get single comments first'
        comment = Comment.objects.get(comment="comment1")
        self.assertIsNotNone(comment, "No comment find")
        self.assertIsNotNone(comment.pubDate)

        user1 = User.objects.get(username="myuser1")
        author1 = Author.objects.get(user=user1)
        post1 = Post.objects.filter(title="title1")[0]

        self.assertEquals(comment.author, author1, "Author did not match")
        self.assertEquals(comment.post, post1, "Post did not match")
        self.assertEquals(comment.comment, "comment1",
                          "Comment did not match")

    def testAllComments(self):
        'check does all the post exists, then check are they correct'

        comment1 = Comment.objects.get(comment="comment1")
        comment2 = Comment.objects.get(comment="comment2")
        comment3 = Comment.objects.get(comment="comment3")
        comment4 = Comment.objects.get(comment="comment4")
        comments = Comment.objects.filter()
        self.assertEqual(len(comments), 4, "all comments find")
        self.assertEquals(comment1.comment, "comment1",
                          "Comment did not match")
        self.assertEquals(comment2.comment, "comment2",
                          "Comment did not match")
        self.assertEquals(comment3.comment, "comment3",
                          "Comment did not match")
        self.assertEquals(comment4.comment, "comment4",
                          "Comment did not match")

    def testDeleteComment(self):
        """
        Tests comment deletion from database
        """
        comment = Comment.objects.get(comment="comment1")
        self.assertIsNotNone(comment, "somthing is here")
        comment=Comment.objects.filter(comment="comment1").delete()
        self.assertIsNone(comment, "shouldnt be anything there")

    def testGetNonExistantComment(self):
        """
        Tests retrieving a non existant comment from the database
        """
        comments = Comment.objects.filter(comment="No good")
        self.assertEquals(len(comments), 0, "This should not exists")


    def testOtherAuthorCanComment(self):
    	post = Post.objects.get(author="author1")
        self.assertIsNotNone(post, "there is a post")
        comment4=Comment.objects.create(
            author=author2,            
            guid=uuid.uuid1(),
            post=post1,
            comment="comment4")
    	self.assertTure(comment4=Comment.objects.create(
            			author=author2,            
            			guid=uuid.uuid1(),
            			post=post1,
           		 		comment="comment4"), "they shold able to comment on others")