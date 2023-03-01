from django.test import *
from service.models.author import Author
from service.models.comment import Comment
from service.models.post import Post
from django.contrib.auth.models import User
from service.views.comment import *
import uuid

from django.urls import reverse

class AuthorTests(TestCase):

    def setUp(self):

        self.comment_view = CommentView()

        self.user1 = User.objects.create_user("joeguy", "joeguy@email.com", "12345")
        self.user2 = User.objects.create_user("somebody", "somebody@email.com", "1234")

        self.author1 = Author.objects.create(displayName = "Joe Guy", host = "http://localhost:8000", user = self.user1)
        self.author2 = Author.objects.create(displayName = "Somebody Else", host = "http://localhost:8000", user = self.user2)

        self.post1 = Post.objects.create(_id=Post.create_post_id(self.author1._id), title="Hello World!", author=self.author1)

        self.comment1 = Comment.objects.create(_id=Comment.create_comment_id(self.author1._id, self.post1._id), comment="This is a comment.", author=self.author1, post=self.post1)
        self.comment2 = Comment.objects.create(_id=Comment.create_comment_id(self.author2._id, self.post1._id), comment="I hate this post!", author=self.author2, post=self.post1)

        self.request_factory = RequestFactory()
    
    def tearDown(self):
        self.user1.delete()
        self.user2.delete()

    def test_get_comments(self):
        self.kwargs = {
            'author_id': self.author1._id,
            'post_id': self.post1._id
        }

        url = reverse('comment_view', kwargs=self.kwargs)

        get_request = self.request_factory.get(url, user = self.user1)
        get_request.user = self.user1

        comment_response = self.comment_view.get(get_request, author_id=self.kwargs["author_id"], post_id=self.kwargs["post_id"])

        self.assertEqual(comment_response.status_code, 200)

        comments_paged = json.loads(comment_response.content)

        self.assertEqual(comments_paged["type"], "comments")
        self.assertIn(f"authors/{self.kwargs['author_id']}/posts/{self.kwargs['post_id']}/comments", comments_paged["id"])
        self.assertIn(f"authors/{self.kwargs['author_id']}/posts/{self.kwargs['post_id']}", comments_paged["post"])

        self.assertTrue("items" in comments_paged)

        comments = comments_paged["items"]

        self.assertEqual(len(comments), 2)
        self.assertEqual(comments[0]["type"], "comment")
        self.assertEqual(comments[0]["comment"], self.comment1.comment)
        self.assertEqual(comments[0]["author"]["id"], str(self.comment1.author._id))

        self.assertEqual(comments[1]["type"], "comment")
        self.assertEqual(comments[1]["comment"], self.comment2.comment)
        self.assertEqual(comments[1]["author"]["id"], str(self.comment2.author._id))

    def test_post_comment(self):
        self.kwargs = {
            'author_id': self.author1._id,
            'post_id': self.post1._id
        }

        url = reverse('comment_view', kwargs=self.kwargs)

        body = {
            "comment": "Actually I loved this post!",
            "contentType": "text/markdown"
        }

        post_request = self.request_factory.post(url, data=json.dumps(body), user = self.user1, content_type = CONTENT_TYPE_JSON)

        comment_response = self.comment_view.post(post_request, author_id=self.kwargs["author_id"], post_id=self.kwargs["post_id"])

        self.assertEqual(comment_response.status_code, 201)

        comments = Comment.objects.all().filter(post=self.post1)

        self.assertEqual(len(comments), 3) #we added 1 more to post1

        self.assertEqual(comments[2].comment, body["comment"])
        self.assertEqual(comments[2].contentType, body["contentType"])
        self.assertTrue(comments[2]._id) #makes sure that the id is not None or empty
    

