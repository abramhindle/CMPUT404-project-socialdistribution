from django.http import response
from backend.apis import *
from backend.models import *

from django.urls import reverse
from django.contrib.auth import authenticate, login

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

USER_LOGIN_URL = reverse('author_login')


class TestCommentViewSet(APITestCase):
    def setUp(self):
        self.test_user1 = User.objects.create_user(
            username='jon',
            password='youknownothing'
        )

        self.test_user2 = User.objects.create_user(
            username='arya',
            password='nonone'
        )

        self.client = APIClient()

        self.author_test1 = Author.objects.create(
            user=self.test_user1,
            displayName='Jon Snow',
            host="http://localhost:8000/",
            github="https://www.github.com/johnSnow"
        )

        self.author_test2 = Author.objects.create(
            user=self.test_user2,
            displayName='Arya Stark',
            host="http://localhost:8000/",
            github="https://www.github.com/AryaStark"
        )

        self.author_test1.save()
        self.author_test2.save()

        # Make User 1 create a POST
        self.test_post1_author1 = Post.objects.create(
            author=self.author_test1,
            title="I dun wannit",
            description="Jon Snow on not wanting the throne",
            content="Some plaintext for Jon",
            contentType="text/plain",
            visibility="PUBLIC",
            unlisted=False,
            categories=[
                "Test",
                "post",
                "author"
            ],
        )

        self.test_post1_author1.save()

        self.test_post_to_comment = Post.objects.create(
            author=self.author_test1,
            title="National Treasure",
            description="Benny Franklin",
            content="Some plaintext for Washington",
            contentType="text/plain",
            visibility="PUBLIC",
            unlisted=False,
            categories=[
                "Test",
                "post",
                "author"
            ],
        )

        self.test_post_to_comment.save()

        # Make a comment on a post
        self.test_comment1 = Comment.objects.create(
            author=self.author_test2,
            post=self.test_post_to_comment,
            comment="This is a genius movie",
            contentType="text/plain",
            post_author=self.author_test1
        )
        self.test_comment1.save()

        self.test_comment2 = Comment.objects.create(
            author=self.author_test1,
            post=self.test_post_to_comment,
            comment="Thank you for agreeing with me",
            contentType="text/plain",
            post_author=self.author_test1
        )
        self.test_comment2.save()

    def test_create_comment_on_post(self):
        """Testing for creating a comment on an existing post made by an author
            by an author
        """
        # forcing authentication of an authors
        self.client.force_authenticate(user=self.author_test1.user)
        self.client.force_authenticate(user=self.author_test2.user)

        comment_request = {
            "type": "comment",
            "author": {
                "type": "author",
                "url": "http://localhost:8000/author/{}".format(self.author_test2.id),
                "host": "http://localhost:8000/",
                "displayName": "Jeff",
                "github": "https://www.github.com/AryaStark"
            },
            "comment": "Hi I am Ygritte",
            'contentType': "text/plain"
        }

        response = self.client.post(
            reverse(
                'comments_object',
                kwargs={
                    'author_id': self.author_test1.id,
                    'post_id': self.test_post1_author1.id
                }
            ),
            comment_request,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_fail_create_comment_on_post(self):
        """Testing for unsucessfully creating a comment on an existing post made by an author
            by an author, by missing information in the request sent
        """
        # forcing authentication of an authors
        self.client.force_authenticate(user=self.author_test1.user)
        self.client.force_authenticate(user=self.author_test2.user)

        comment_request = {
            "type": "comment",
            "author": {
                "type": "author",
                "url": "http://localhost:8000/author/{}".format(self.author_test2.id),
                "host": "http://localhost:8000/",
                "displayName": "Jeff",
                "github": "https://www.github.com/AryaStark"
            },
            "contentType": "text/plain",
            "comment": "",
        }

        response = self.client.post(
            reverse(
                'comments_object',
                kwargs={
                    'author_id': self.author_test1.id,
                    'post_id': 'aa5d8caa15954e42a39698588f0c473e'
                }
            ),
            comment_request,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_listed_comments(self):
        """Tests to return a paginated list of all comments made on a post specified
        """
        # forcing authentication of an author
        self.client.force_authenticate(user=self.author_test1.user)

        response = self.client.get(
            reverse(
                'comments_object',
                kwargs={
                    'author_id': self.author_test1.id,
                    'post_id': self.test_post_to_comment.id
                }
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
