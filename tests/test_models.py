import uuid
from django.test import TestCase
from django.contrib.auth.models import User
from backend.models import Author, Post, Comment, PostLike, CommentLike

class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create_user("TestUser")
        user_1_id = "2f91a911-850f-4655-ac29-9115822c72a8"
        post_1_id = "8de1673c-3385-11ec-8d3d-0242ac130003"
        comment_1_id ="b9ad7f9e-3386-11ec-8d3d-0242ac130003"
        
        Author.objects.create(
            id=user_1_id,
            user=user,
            url="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a8",
            host="http://127.0.0.1:8000/",
            display_name="Test unit",
        )
        
        Post.objects.create(
            id=post_1_id,
            author=Author.objects.get(id=user_1_id),
            title="post_unit_test",
            source="8de1673c-3385-11ec-8d3d-0242ac130003",
            origin="8de1673c-3385-11ec-8d3d-0242ac130003",
            description="post description",
            content="this is a test",
            url="",
            contentType="image/jpeg;base64",
            visibility="PRIVATE",
            published="date published", # test this
        )
        
        Comment.objects.create(
            id=comment_1_id,
            url="",
            post=Post.objects.get(id=post_1_id),
            author=Author.objects.get(id=user_1_id),
            contentType="text/plain",
            comment="this is a comment test",
            published="",
        )
        
        PostLike.objects.create(
            post=Post.objects.get(id=post_1_id),
            author=Author.objects.get(id=user_1_id),
            summary=""
        )
        
        CommentLike.objects.create(
            author=Author.objects.get(id=user_1_id),
            comment=Comment.objects.get(id=comment_1_id),
            summary=""
        )
        
    def test_display_name(self):
        author = Author.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a8")
        field_label = author.display_name
        self.assertEqual(field_label, 'Test unit')

    
    def test_post(self):
        post = Post.objects.get(id="8de1673c-3385-11ec-8d3d-0242ac130003")
        self.assertTrue(isinstance(post, Post))
        self.assertTrue(isinstance(post.author, Author))
        
        self.assertEqual(post.title, "post_unit_test")
        self.assertEqual(post.content, "this is a test")
        self.assertEqual(post.source, "8de1673c-3385-11ec-8d3d-0242ac130003")
        self.assertEqual(post.origin, "8de1673c-3385-11ec-8d3d-0242ac130003")
        self.assertEqual(post.visibility, "PRIVATE")
        self.assertEqual(post.contentType, "image/jpeg;base64")

    def test_comment(self):
        comment = Comment.objects.get(id="b9ad7f9e-3386-11ec-8d3d-0242ac130003")
        self.assertTrue(isinstance(comment, Comment))
        self.assertTrue(isinstance(comment.author, Author))
        self.assertTrue(isinstance(comment.post, Post))
        
        self.assertEqual(comment.contentType, "text/plain")
        self.assertEqual(comment.comment, "this is a comment test")
    
    def test_post_like(self):
        # am I right to use post's id?
        post_like = PostLike.objects.get(post="8de1673c-3385-11ec-8d3d-0242ac130003")
        self.assertTrue(isinstance(post_like, PostLike))
        self.assertTrue(isinstance(post_like.author, Author))
        self.assertTrue(isinstance(post_like.post, Post))
    
    def test_comment_like(self):
        comment_like = CommentLike.objects.get(comment="b9ad7f9e-3386-11ec-8d3d-0242ac130003")
        self.assertTrue(isinstance(comment_like, CommentLike))
        self.assertTrue(isinstance(comment_like.author, Author))
        self.assertTrue(isinstance(comment_like.comment, Comment))