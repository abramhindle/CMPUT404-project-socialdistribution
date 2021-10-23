import uuid
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from backend.models import Author, Post, Comment, PostLike, CommentLike, InboxPost, InboxPostLike, InboxCommentLike



class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        uuid_list = [
            "95a1e643-180c-4de6-8fc5-9cb48a216fbe",
            "856c692d-2514-4d06-80fc-4c4312188db3",
        ]
        number_of_authors = len(uuid_list)
        User.objects.bulk_create([
            User(username="AuthorViewTest_{}".format(idx),
            password=make_password("Margret Thatcher"),
            is_active=True
            ) for idx in range(number_of_authors)
        ])
        for author_id in range(number_of_authors):
            Author.objects.create(
                id=uuid_list[author_id],
                user=User.objects.get(username="AuthorViewTest_{}".format(author_id)),
                display_name="Test unit{}".format(author_id),
                url="http://127.0.0.1:8000/author/{}".format(uuid_list[author_id]),
                host="http://127.0.0.1:8000/",
            )
    def test_display_name(self):
        author = Author.objects.get(id="95a1e643-180c-4de6-8fc5-9cb48a216fbe")
        field_label = author.display_name
        self.assertEqual(field_label, 'Test unit0')
        author = Author.objects.get(id="856c692d-2514-4d06-80fc-4c4312188db3")
        field_label = author.display_name
        self.assertEqual(field_label, 'Test unit1')

class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create_user("TestUser")
        testAuthor = Author.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a8",
            user=user,
            url="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a8",
            host="http://127.0.0.1:8000/",
            display_name="Test unit",
        )
        Post.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a9",
            url="http://127.0.0.1:8000/post/2f91a911-850f-4655-ac29-9115822c72a9",
            title="Test Title",
            source = "https://www.youtube.com/watch?v=YIJI5U0BWr0",
            origin = "https://www.django-rest-framework.org/api-guide/views/",
            description = "Test Post",
            contentType = "text/plain",
            content = "test text",
            author = testAuthor,
        )
    def test_title(self):
        post = Post.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a9")
        field_label = post.title
        self.assertEqual(field_label, 'Test Title')
    def test_author(self):
        post = Post.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a9")
        expected_author = Author.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a8")
        post_associated_author_label = post.author.display_name
        expected_author_label = expected_author.display_name
        self.assertEqual(post_associated_author_label, expected_author_label)

class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        post_user = User.objects.create_user("PostUser")
        post_author = Author.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a8",
            user=post_user,
            url="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a8",
            host="http://127.0.0.1:8000/",
            display_name="Test unit",
        )
        comment_user = User.objects.create_user("CommentUser")
        comment_author = Author.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a6",
            user=comment_user,
            url="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a6",
            host="http://127.0.0.1:8000/",
            display_name="Test unit",
        )
        post = Post.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a9",
            url="http://127.0.0.1:8000/post/2f91a911-850f-4655-ac29-9115822c72a9",
            title="Test Title",
            source = "https://www.youtube.com/watch?v=YIJI5U0BWr0",
            origin = "https://www.django-rest-framework.org/api-guide/views/",
            description = "Test Post",
            contentType = "text/plain",
            content = "test text",
            author = post_author,
        )
        Comment.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a7",
            url="http://127.0.0.1:8000/comment/2f91a911-850f-4655-ac29-9115822c72a7",
            post = post,
            author = comment_author,
            comment = "This is a test comment",
        )
    def test_comment(self):
        comment = Comment.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a7")
        comment_text = comment.comment
        self.assertEqual(comment_text, "This is a test comment")
    def test_correct_comment_post_author(self):
        comment = Comment.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a7")
        expected_author = Author.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a8")
        comment_post_associated_author_label = comment.post.author.display_name
        expected_author_label = expected_author.display_name
        self.assertEqual(comment_post_associated_author_label, expected_author_label)
    def test_post_comments(self):
        post = Post.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a9")
        #help for this from https://www.codegrepper.com/code-examples/python/check+if+a+value+exist+in+a+model+Django
        self.assertEqual(True, post.comments.all().filter(id="2f91a911-850f-4655-ac29-9115822c72a7").exists())

class PostLikeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        post_user = User.objects.create_user("PostUser")
        post_author = Author.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a8",
            user=post_user,
            url="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a8",
            host="http://127.0.0.1:8000/",
            display_name="Test unit",
        )
        liking_user = User.objects.create_user("LikingUser")
        liking_author = Author.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a6",
            user=liking_user,
            url="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a6",
            host="http://127.0.0.1:8000/",
            display_name="Test unit",
        )
        post = Post.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a9",
            url="http://127.0.0.1:8000/post/2f91a911-850f-4655-ac29-9115822c72a9",
            title="Test Title",
            source = "https://www.youtube.com/watch?v=YIJI5U0BWr0",
            origin = "https://www.django-rest-framework.org/api-guide/views/",
            description = "Test Post",
            contentType = "text/plain",
            content = "test text",
            author = post_author,
        )
        post_like = PostLike.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a5",
            post = post,
            author = liking_author,
            summary = "liking author likes post",
        )
    def test_post_like_by_liking_author(self):
        #checks to see if our post has knowledge that it was liked by the liking_author
        post = Post.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a9")
        #help for this from https://www.codegrepper.com/code-examples/python/check+if+a+value+exist+in+a+model+Django
        self.assertEqual(True, post.likes.all().filter(author="2f91a911-850f-4655-ac29-9115822c72a6").exists())

class CommentLikeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        post_user = User.objects.create_user("PostUser")
        post_author = Author.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a8",
            user=post_user,
            url="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a8",
            host="http://127.0.0.1:8000/",
            display_name="Test unit",
        )
        liking_user = User.objects.create_user("LikingUser")
        liking_author = Author.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a6",
            user=liking_user,
            url="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a6",
            host="http://127.0.0.1:8000/",
            display_name="Test unit",
        )
        comment_user = User.objects.create_user("CommentUser")
        comment_author = Author.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a4",
            user=comment_user,
            url="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a4",
            host="http://127.0.0.1:8000/",
            display_name="Test unit",
        )
        post = Post.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a9",
            url="http://127.0.0.1:8000/post/2f91a911-850f-4655-ac29-9115822c72a9",
            title="Test Title",
            source = "https://www.youtube.com/watch?v=YIJI5U0BWr0",
            origin = "https://www.django-rest-framework.org/api-guide/views/",
            description = "Test Post",
            contentType = "text/plain",
            content = "test text",
            author = post_author,
        )
        comment= Comment.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a7",
            url="http://127.0.0.1:8000/comment/2f91a911-850f-4655-ac29-9115822c72a7",
            post = post,
            author = comment_author,
            comment = "This is a test comment",
        )
        comment_like = CommentLike.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a5",
            comment = comment,
            author = liking_author,
            summary = "liking author likes post",
        )
    def test_comment_like_by_liking_author(self):
        #checks to see if our comment has knowledge that it was liked by the liking_author
        comment = Comment.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a7")
        #help for this from https://www.codegrepper.com/code-examples/python/check+if+a+value+exist+in+a+model+Django
        self.assertEqual(True, comment.likes.all().filter(author="2f91a911-850f-4655-ac29-9115822c72a6").exists())

class InboxPostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        post_user = User.objects.create_user("PostUser")
        post_author = Author.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a8",
            user=post_user,
            url="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a8",
            host="http://127.0.0.1:8000/",
            display_name="Test unit",
        )
        inbox_owner_user = User.objects.create_user("InboxUser")
        inbox_owner_author = Author.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a6",
            user=inbox_owner_user,
            url="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a6",
            host="http://127.0.0.1:8000/",
            display_name="Test unit",
        )
        post = Post.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a9",
            url="http://127.0.0.1:8000/post/2f91a911-850f-4655-ac29-9115822c72a9",
            title="Test Title",
            source = "https://www.youtube.com/watch?v=YIJI5U0BWr0",
            origin = "https://www.django-rest-framework.org/api-guide/views/",
            description = "Test Post",
            contentType = "text/plain",
            content = "test text",
            author = post_author,
        )
        inbox_post = InboxPost.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a5",
            post = post,
            author = inbox_owner_author,
        )
    def test_post_in_inbox(self):
        #checks to see if our author has knowledge that a post is in their inbox
        author = Author.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a6")
        #help for this from https://www.codegrepper.com/code-examples/python/check+if+a+value+exist+in+a+model+Django
        self.assertEqual(True, author.posts_in_inbox.all().filter(post="2f91a911-850f-4655-ac29-9115822c72a9").exists())

class InboxPostLikeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods

        #here the posting author is the same as the inbox owning author
        post_user = User.objects.create_user("PostUser")
        post_author = Author.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a8",
            user=post_user,
            url="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a8",
            host="http://127.0.0.1:8000/",
            display_name="Test unit",
        )
        liking_user = User.objects.create_user("LikingUser")
        liking_author = Author.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a6",
            user=liking_user,
            url="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a6",
            host="http://127.0.0.1:8000/",
            display_name="Test unit",
        )
        post = Post.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a9",
            url="http://127.0.0.1:8000/post/2f91a911-850f-4655-ac29-9115822c72a9",
            title="Test Title",
            source = "https://www.youtube.com/watch?v=YIJI5U0BWr0",
            origin = "https://www.django-rest-framework.org/api-guide/views/",
            description = "Test Post",
            contentType = "text/plain",
            content = "test text",
            author = post_author,
        )
        post_like = PostLike.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a5",
            post = post,
            author = liking_author,
            summary = "liking author likes post",
        )
        inbox_post_like = InboxPostLike.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a4",
            post_like = post_like,
            author = post_author,
        )
    def test_post_like_in_inbox(self):
        #checks to see if our author has knowledge that a post like is in their inbox
        author = Author.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a8")
        #help for this from https://www.codegrepper.com/code-examples/python/check+if+a+value+exist+in+a+model+Django
        self.assertEqual(True, author.post_likes_in_inbox.all().filter(post_like="2f91a911-850f-4655-ac29-9115822c72a5").exists())

class InboxPostLikeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        post_user = User.objects.create_user("PostUser")
        post_author = Author.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a8",
            user=post_user,
            url="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a8",
            host="http://127.0.0.1:8000/",
            display_name="Test unit",
        )
        liking_user = User.objects.create_user("LikingUser")
        liking_author = Author.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a6",
            user=liking_user,
            url="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a6",
            host="http://127.0.0.1:8000/",
            display_name="Test unit",
        )
        #here the posting author is the same as the inbox owning author
        comment_user = User.objects.create_user("CommentUser")
        comment_author = Author.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a4",
            user=comment_user,
            url="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a4",
            host="http://127.0.0.1:8000/",
            display_name="Test unit",
        )
        post = Post.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a9",
            url="http://127.0.0.1:8000/post/2f91a911-850f-4655-ac29-9115822c72a9",
            title="Test Title",
            source = "https://www.youtube.com/watch?v=YIJI5U0BWr0",
            origin = "https://www.django-rest-framework.org/api-guide/views/",
            description = "Test Post",
            contentType = "text/plain",
            content = "test text",
            author = post_author,
        )
        comment= Comment.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a7",
            url="http://127.0.0.1:8000/comment/2f91a911-850f-4655-ac29-9115822c72a7",
            post = post,
            author = comment_author,
            comment = "This is a test comment",
        )
        comment_like = CommentLike.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a5",
            comment = comment,
            author = liking_author,
            summary = "liking author likes post",
        )
        inbox_comment_like = InboxCommentLike.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a3",
            comment_like = comment_like,
            author = comment_author,
        )
    def test_comment_like_in_inbox(self):
        #checks to see if our author has knowledge that a comment like is in their inbox
        author = Author.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a4")
        #help for this from https://www.codegrepper.com/code-examples/python/check+if+a+value+exist+in+a+model+Django
        self.assertEqual(True, author.comment_likes_in_inbox.all().filter(comment_like="2f91a911-850f-4655-ac29-9115822c72a5").exists())
