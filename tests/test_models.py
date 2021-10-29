import uuid
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from backend.models import Author, Post, Comment, Like



class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        uuid_list = [
            "95a1e643-180c-4de6-8fc5-9cb48a216fbe",
            "856c692d-2514-4d06-80fc-4c4312188db3",
        ]
        number_of_authors = len(uuid_list)
        user = User.objects.bulk_create([
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
    def test_host(self):
        author = Author.objects.get(id="95a1e643-180c-4de6-8fc5-9cb48a216fbe")
        field_label = author.host
        self.assertEqual(field_label, 'http://127.0.0.1:8000/')
    def test_url(self):
        author = Author.objects.get(id="95a1e643-180c-4de6-8fc5-9cb48a216fbe")
        field_label = author.url
        self.assertEqual(field_label, 'http://127.0.0.1:8000/author/95a1e643-180c-4de6-8fc5-9cb48a216fbe')
    def testUser(self):
        author = Author.objects.get(id="95a1e643-180c-4de6-8fc5-9cb48a216fbe")
        right_user = User.objects.get(username = "AuthorViewTest_0")
        wrong_user = User.objects.get(username = "AuthorViewTest_1")
        author_user = author.user
        self.assertEqual(author_user, right_user)
        self.assertNotEqual(author_user, wrong_user)


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        uuid_list = [
            "2f91a911-850f-4655-ac29-9115822c72a8",
            "2f91a911-850f-4655-ac29-9115822c72b8",
        ]
        number_of_authors = len(uuid_list)
        User.objects.bulk_create([
            User(username="LoginViewTest{}".format(idx),
            password=make_password("Margret Thatcher"),
            is_active = False if idx == 2 else True
            ) for idx in range(number_of_authors)
        ])
        authors = []
        for author_id in range(number_of_authors):
                authors.append(Author.objects.create(
                id=uuid_list[author_id],
                user=User.objects.get(username="LoginViewTest{}".format(author_id)),
                display_name="Test unit{}".format(author_id),
                url="http://127.0.0.1:8000/author/{}".format(uuid_list[author_id]),
                host="http://127.0.0.1:8000/",
            ))
        Post.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a9",
            url="http://127.0.0.1:8000/post/2f91a911-850f-4655-ac29-9115822c72a9",
            title="Test Title",
            source = "https://www.youtube.com/watch?v=YIJI5U0BWr0",
            origin = "https://www.django-rest-framework.org/api-guide/views/",
            description = "Test Post",
            content_type = "text/plain",
            content = "test text",
            author = authors[0],
        )
        Post.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72b9",
            url="http://127.0.0.1:8000/post/2f91a911-850f-4655-ac29-9115822c72b9",
            title="Test Title",
            source = "https://www.youtube.com/watch?v=YIJI5U0BWr0",
            origin = "https://www.django-rest-framework.org/api-guide/views/",
            description = "Test Post",
            content_type = "text/plain",
            content = "test text",
            author = authors[1],
        )
    def test_title(self):
        post = Post.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a9")
        field_label = post.title
        self.assertEqual(field_label, 'Test Title')
    def test_url(self):
        post = Post.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a9")
        post_url = post.url
        self.assertEqual(post_url, "http://127.0.0.1:8000/post/2f91a911-850f-4655-ac29-9115822c72a9")
    def test_author(self):
        post = Post.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a9")
        expected_author = Author.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a8")
        post_associated_author = post.author
        self.assertEqual(post_associated_author, expected_author)
    def test_post_in_author_posted(self):
        post = Post.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a9")
        author = Author.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a8")
        self.assertEqual(post, author.posted.get(id="2f91a911-850f-4655-ac29-9115822c72a9"))
    def test_post_not_in_different_author_posted(self):
        author = Author.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a8")
        #help for this from https://www.codegrepper.com/code-examples/python/check+if+a+value+exist+in+a+model+Django
        self.assertNotEqual(True, author.posted.all().filter(id="2f91a911-850f-4655-ac29-9115822c72b9").exists())
        

class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        uuid_list = [
            "2f91a911-850f-4655-ac29-9115822c72a8",
            "2f91a911-850f-4655-ac29-9115822c72a6",
        ]
        number_of_authors = len(uuid_list)
        User.objects.bulk_create([
            User(username="LoginViewTest{}".format(idx),
            password=make_password("Margret Thatcher"),
            is_active = False if idx == 2 else True
            ) for idx in range(number_of_authors)
        ])
        authors = []
        for author_id in range(number_of_authors):
                authors.append(Author.objects.create(
                id=uuid_list[author_id],
                user=User.objects.get(username="LoginViewTest{}".format(author_id)),
                display_name="Test unit{}".format(author_id),
                url="http://127.0.0.1:8000/author/{}".format(uuid_list[author_id]),
                host="http://127.0.0.1:8000/",
            ))
        post = Post.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a9",
            url="http://127.0.0.1:8000/post/2f91a911-850f-4655-ac29-9115822c72a9",
            title="Test Title",
            source = "https://www.youtube.com/watch?v=YIJI5U0BWr0",
            origin = "https://www.django-rest-framework.org/api-guide/views/",
            description = "Test Post",
            content_type = "text/plain",
            content = "test text",
            author = authors[0],
        )
        Post.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72b9",
            url="http://127.0.0.1:8000/post/2f91a911-850f-4655-ac29-9115822c72b9",
            title="Test Title",
            source = "https://www.youtube.com/watch?v=YIJI5U0BWr0",
            origin = "https://www.django-rest-framework.org/api-guide/views/",
            description = "Test Post",
            content_type = "text/plain",
            content = "test text",
            author = authors[0],
        )
        Comment.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a7",
            url="http://127.0.0.1:8000/comment/2f91a911-850f-4655-ac29-9115822c72a7",
            post = post,
            author = authors[1],
            comment = "This is a test comment",
        )
        Comment.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72b7",
            url="http://127.0.0.1:8000/comment/2f91a911-850f-4655-ac29-9115822c72b7",
            post = post,
            author = authors[1],
            comment = "This is a test comment2",
        )
    def test_comment(self):
        comment = Comment.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a7")
        comment_text = comment.comment
        self.assertEqual(comment_text, "This is a test comment")
    def test_url(self):
        comment = Comment.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a7")
        comment_url = comment.url
        self.assertEqual(comment_url, "http://127.0.0.1:8000/comment/2f91a911-850f-4655-ac29-9115822c72a7")
    def test_author(self):
        comment = Comment.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a7")
        expected_author = Author.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a6")
        comment_associated_author = comment.author
        self.assertEqual(comment_associated_author, expected_author)
    def test_correct_comment_post_author(self):
        comment = Comment.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a7")
        expected_author = Author.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a8")
        comment_post_associated_author = comment.post.author
        self.assertEqual(comment_post_associated_author, expected_author)
    def test_comment_in_post_comments(self):
        comment = Comment.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a7")
        post = Post.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a9")
        self.assertEqual(comment, post.comments.get(id="2f91a911-850f-4655-ac29-9115822c72a7"))
    def test_comment_not_in_different_post_comments(self):
        comment = Comment.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a7")
        post = Post.objects.get(id="2f91a911-850f-4655-ac29-9115822c72b9")
        self.assertNotEqual(True, post.comments.all().filter(id="2f91a911-850f-4655-ac29-9115822c72a7").exists())
    def correct_number_comments_in_post_comments(self):
        comment = Comment.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a7")
        post = Post.objects.get(id="2f91a911-850f-4655-ac29-9115822c72b9")
        self.assertEqual(2, len(post.comments.all()))

class PostLikeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        uuid_list = [
            "2f91a911-850f-4655-ac29-9115822c72a8",
            "2f91a911-850f-4655-ac29-9115822c72a6",
        ]
        number_of_authors = len(uuid_list)
        User.objects.bulk_create([
            User(username="LoginViewTest{}".format(idx),
            password=make_password("Margret Thatcher"),
            is_active = False if idx == 2 else True
            ) for idx in range(number_of_authors)
        ])
        authors = []
        for author_id in range(number_of_authors):
                authors.append(Author.objects.create(
                id=uuid_list[author_id],
                user=User.objects.get(username="LoginViewTest{}".format(author_id)),
                display_name="Test unit{}".format(author_id),
                url="http://127.0.0.1:8000/author/{}".format(uuid_list[author_id]),
                host="http://127.0.0.1:8000/",
            ))
        post = Post.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a9",
            url="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a8/post/2f91a911-850f-4655-ac29-9115822c72a9",
            title="Test Title",
            source = "https://www.youtube.com/watch?v=YIJI5U0BWr0",
            origin = "https://www.django-rest-framework.org/api-guide/views/",
            description = "Test Post",
            content_type = "text/plain",
            content = "test text",
            author = authors[0],
        )
        post_like = Like.objects.create(
            object="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a8/post/2f91a911-850f-4655-ac29-9115822c72a9",
            post = post,
            author = authors[1],
            summary = "liking author likes post",
        )
    def test_summary(self):
        post_like = Like.objects.get(object="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a8/post/2f91a911-850f-4655-ac29-9115822c72a9")
        post_like_summary = post_like.summary
        self.assertEqual(post_like_summary, "liking author likes post")
    def test_author(self):
        post_like = Like.objects.get(object="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a8/post/2f91a911-850f-4655-ac29-9115822c72a9")
        post_like_author = post_like.author
        expected_author = Author.objects.get(id = "2f91a911-850f-4655-ac29-9115822c72a6")
        self.assertEqual(post_like_author, expected_author)
    def test_post(self):
        post_like = Like.objects.get(object="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a8/post/2f91a911-850f-4655-ac29-9115822c72a9")
        post_like_post = post_like.post
        expected_post = Post.objects.get(id = "2f91a911-850f-4655-ac29-9115822c72a9")
        self.assertEqual(expected_post, post_like_post)
    def test_post_like_by_liking_author(self):
        #checks to see if our post has knowledge that it was liked by the liking_author
        post_like = Like.objects.get(object="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a8/post/2f91a911-850f-4655-ac29-9115822c72a9")
        post = Post.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a9")
        self.assertEqual(post_like, post.likes.get(object="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a8/post/2f91a911-850f-4655-ac29-9115822c72a9"))
    def test_like_in_liking_author_posts_liked(self):
        post_like = Like.objects.get(object="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a8/post/2f91a911-850f-4655-ac29-9115822c72a9")
        author = Author.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a6")
        self.assertEqual(post_like, author.liked.get(object="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a8/post/2f91a911-850f-4655-ac29-9115822c72a9"))

class CommentLikeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        uuid_list = [
            "2f91a911-850f-4655-ac29-9115822c72a8",
            "2f91a911-850f-4655-ac29-9115822c72a6",
            "2f91a911-850f-4655-ac29-9115822c72a4",
        ]
        number_of_authors = len(uuid_list)
        User.objects.bulk_create([
            User(username="LoginViewTest{}".format(idx),
            password=make_password("Margret Thatcher"),
            is_active = False if idx == 2 else True
            ) for idx in range(number_of_authors)
        ])
        authors = []
        for author_id in range(number_of_authors):
                authors.append(Author.objects.create(
                id=uuid_list[author_id],
                user=User.objects.get(username="LoginViewTest{}".format(author_id)),
                display_name="Test unit{}".format(author_id),
                url="http://127.0.0.1:8000/author/{}".format(uuid_list[author_id]),
                host="http://127.0.0.1:8000/",
            ))
        post = Post.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a9",
            url="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a8/post/2f91a911-850f-4655-ac29-9115822c72a9",
            title="Test Title",
            source = "https://www.youtube.com/watch?v=YIJI5U0BWr0",
            origin = "https://www.django-rest-framework.org/api-guide/views/",
            description = "Test Post",
            content_type = "text/plain",
            content = "test text",
            author = authors[0],
        )
        comment= Comment.objects.create(
            id="2f91a911-850f-4655-ac29-9115822c72a7",
            url="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a8/post/2f91a911-850f-4655-ac29-9115822c72a9/comment/2f91a911-850f-4655-ac29-9115822c72a7",
            post = post,
            author = authors[2],
            comment = "This is a test comment",
        )
        comment_like = Like.objects.create(
            object="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a8/post/2f91a911-850f-4655-ac29-9115822c72a9/comment/2f91a911-850f-4655-ac29-9115822c72a7",
            comment = comment,
            author = authors[1],
            summary = "liking author likes comment",
        )
    def test_summary(self):
        comment_like = Like.objects.get(object="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a8/post/2f91a911-850f-4655-ac29-9115822c72a9/comment/2f91a911-850f-4655-ac29-9115822c72a7")
        comment_like_summary = comment_like.summary
        self.assertEqual(comment_like_summary, "liking author likes comment")
    def test_author(self):
        comment_like = Like.objects.get(object="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a8/post/2f91a911-850f-4655-ac29-9115822c72a9/comment/2f91a911-850f-4655-ac29-9115822c72a7")
        comment_like_author = comment_like.author
        expected_author = Author.objects.get(id = "2f91a911-850f-4655-ac29-9115822c72a6")
        self.assertEqual(comment_like_author, expected_author)
    def test_comment(self):
        comment_like = Like.objects.get(object="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a8/post/2f91a911-850f-4655-ac29-9115822c72a9/comment/2f91a911-850f-4655-ac29-9115822c72a7")
        comment_like_comment = comment_like.comment
        expected_comment = Comment.objects.get(id = "2f91a911-850f-4655-ac29-9115822c72a7")
        self.assertEqual(expected_comment, comment_like_comment)
    def test_comment_like_by_liking_author(self):
        #checks to see if our comment has knowledge that it was liked by the liking_author
        comment_like = Like.objects.get(object="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a8/post/2f91a911-850f-4655-ac29-9115822c72a9/comment/2f91a911-850f-4655-ac29-9115822c72a7")
        comment = Comment.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a7")
        self.assertEqual(comment_like, comment.likes.get(object="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a8/post/2f91a911-850f-4655-ac29-9115822c72a9/comment/2f91a911-850f-4655-ac29-9115822c72a7"))
    def test_like_in_liking_author_comments_liked(self):
        comment_like = Like.objects.get(object="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a8/post/2f91a911-850f-4655-ac29-9115822c72a9/comment/2f91a911-850f-4655-ac29-9115822c72a7")
        author = Author.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a6")
        self.assertEqual(comment_like, author.liked.get(object="http://127.0.0.1:8000/author/2f91a911-850f-4655-ac29-9115822c72a8/post/2f91a911-850f-4655-ac29-9115822c72a9/comment/2f91a911-850f-4655-ac29-9115822c72a7"))

#class InboxPostModelTest(TestCase):
#    @classmethod
#    def setUpTestData(cls):
#        # Set up non-modified objects used by all test methods
#        uuid_list = [
#            "2f91a911-850f-4655-ac29-9115822c72a8",
#            "2f91a911-850f-4655-ac29-9115822c72a6",
#        ]
#        number_of_authors = len(uuid_list)
#        User.objects.bulk_create([
#            User(username="LoginViewTest{}".format(idx),
#            password=make_password("Margret Thatcher"),
#            is_active = False if idx == 2 else True
#            ) for idx in range(number_of_authors)
#        ])
#        authors = []
#        for author_id in range(number_of_authors):
#                authors.append(Author.objects.create(
#                id=uuid_list[author_id],
#                user=User.objects.get(username="LoginViewTest{}".format(author_id)),
#                display_name="Test unit{}".format(author_id),
#                url="http://127.0.0.1:8000/author/{}".format(uuid_list[author_id]),
#                host="http://127.0.0.1:8000/",
#            ))
#        post = Post.objects.create(
#            id="2f91a911-850f-4655-ac29-9115822c72a9",
#            url="http://127.0.0.1:8000/post/2f91a911-850f-4655-ac29-9115822c72a9",
#            title="Test Title",
#            source = "https://www.youtube.com/watch?v=YIJI5U0BWr0",
#            origin = "https://www.django-rest-framework.org/api-guide/views/",
#            description = "Test Post",
#            content_type = "text/plain",
#            content = "test text",
#            author = authors[0],
#        )
#        inbox_post = InboxPost.objects.create(
#            id="2f91a911-850f-4655-ac29-9115822c72a5",
#            post = post,
#            author = authors[1],
#        )
#    def test_post_in_inbox(self):
        #checks to see if our author has knowledge that a post is in their inbox
#        author = Author.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a6")
        #help for this from https://www.codegrepper.com/code-examples/python/check+if+a+value+exist+in+a+model+Django
#        self.assertEqual(True, author.posts_in_inbox.all().filter(post="2f91a911-850f-4655-ac29-9115822c72a9").exists())

#class InboxPostLikeModelTest(TestCase):
#    @classmethod
#    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods

        #here the posting author is the same as the inbox owning author
#        uuid_list = [
#            "2f91a911-850f-4655-ac29-9115822c72a8",
#            "2f91a911-850f-4655-ac29-9115822c72a6",
#        ]
 #       number_of_authors = len(uuid_list)
 #       User.objects.bulk_create([
 #           User(username="LoginViewTest{}".format(idx),
 #           password=make_password("Margret Thatcher"),
 #           is_active = False if idx == 2 else True
 #           ) for idx in range(number_of_authors)
 #       ])
 #       authors = []
 #       for author_id in range(number_of_authors):
 #               authors.append(Author.objects.create(
 #               id=uuid_list[author_id],
 #               user=User.objects.get(username="LoginViewTest{}".format(author_id)),
 #               display_name="Test unit{}".format(author_id),
 #               url="http://127.0.0.1:8000/author/{}".format(uuid_list[author_id]),
 #               host="http://127.0.0.1:8000/",
 #           ))
 #       post = Post.objects.create(
#            id="2f91a911-850f-4655-ac29-9115822c72a9",
#            url="http://127.0.0.1:8000/post/2f91a911-850f-4655-ac29-9115822c72a9",
#            title="Test Title",
#            source = "https://www.youtube.com/watch?v=YIJI5U0BWr0",
#            origin = "https://www.django-rest-framework.org/api-guide/views/",
#            description = "Test Post",
#            content_type = "text/plain",
#            content = "test text",
#            author = authors[0],
#        )
#        post_like = PostLike.objects.create(
#            id="2f91a911-850f-4655-ac29-9115822c72a5",
#            post = post,
#            author = authors[1],
#            summary = "liking author likes post",
#        )
#        inbox_post_like = InboxPostLike.objects.create(
#            id="2f91a911-850f-4655-ac29-9115822c72a4",
#            post_like = post_like,
#            author = authors[0],
#        )
#    def test_post_like_in_inbox(self):
#        #checks to see if our author has knowledge that a post like is in their inbox
#        author = Author.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a8")
#        #help for this from https://www.codegrepper.com/code-examples/python/check+if+a+value+exist+in+a+model+Django
#        self.assertEqual(True, author.post_likes_in_inbox.all().filter(post_like="2f91a911-850f-4655-ac29-9115822c72a5").exists())

#class InboxCommentLikeModelTest(TestCase):
#    @classmethod
#    def setUpTestData(cls):
#        # Set up non-modified objects used by all test methods
#        uuid_list = [
#            "2f91a911-850f-4655-ac29-9115822c72a8",
#            "2f91a911-850f-4655-ac29-9115822c72a6",
#            "2f91a911-850f-4655-ac29-9115822c72a4",
#        ]
#        number_of_authors = len(uuid_list)
#        User.objects.bulk_create([
#            User(username="LoginViewTest{}".format(idx),
#            password=make_password("Margret Thatcher"),
#            is_active = False if idx == 2 else True
#            ) for idx in range(number_of_authors)
#        ])
#        authors = []
#        for author_id in range(number_of_authors):
#                authors.append(Author.objects.create(
#                id=uuid_list[author_id],
#                user=User.objects.get(username="LoginViewTest{}".format(author_id)),
#                display_name="Test unit{}".format(author_id),
#                url="http://127.0.0.1:8000/author/{}".format(uuid_list[author_id]),
#                host="http://127.0.0.1:8000/",
#            ))
#        post = Post.objects.create(
#            id="2f91a911-850f-4655-ac29-9115822c72a9",
#            url="http://127.0.0.1:8000/post/2f91a911-850f-4655-ac29-9115822c72a9",
#            title="Test Title",
#            source = "https://www.youtube.com/watch?v=YIJI5U0BWr0",
#            origin = "https://www.django-rest-framework.org/api-guide/views/",
#            description = "Test Post",
#           content_type = "text/plain",
#            content = "test text",
#            author = authors[0],
#        )
#        comment= Comment.objects.create(
#            id="2f91a911-850f-4655-ac29-9115822c72a7",
#            url="http://127.0.0.1:8000/comment/2f91a911-850f-4655-ac29-9115822c72a7",
#            post = post,
#            author = authors[2],
#            comment = "This is a test comment",
#        )
#        comment_like = CommentLike.objects.create(
#            id="2f91a911-850f-4655-ac29-9115822c72a5",
#            comment = comment,
#            author = authors[1],
#            summary = "liking author likes post",
#        )
#        inbox_comment_like = InboxCommentLike.objects.create(
#            id="2f91a911-850f-4655-ac29-9115822c72a3",
#            comment_like = comment_like,
#            author = authors[2],
#        )
    #def test_comment_like_in_inbox(self):
        #checks to see if our author has knowledge that a comment like is in their inbox
    #    author = Author.objects.get(id="2f91a911-850f-4655-ac29-9115822c72a4")
        #help for this from https://www.codegrepper.com/code-examples/python/check+if+a+value+exist+in+a+model+Django
    #    self.assertEqual(True, author.comment_likes_in_inbox.all().filter(comment_like="2f91a911-850f-4655-ac29-9115822c72a5").exists())


