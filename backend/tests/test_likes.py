from django.http import response
from backend.apis import *
from backend.models import *

from django.urls import reverse
from django.contrib.auth import authenticate, login

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

USER_LOGIN_URL = reverse('author_login')


class TestLikeAPI(APITestCase):
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

        self.test_private_post = Post.objects.create(
            author=self.author_test1,
            title="National Treasure",
            description="Benny Franklin",
            content="Some plaintext for Washington",
            contentType="text/plain",
            visibility="FRIENDS",
            unlisted=False,
            categories=[
                "Test",
                "post",
                "author"
            ],
        )

        self.test_private_post.save()

        self.test_post_to_comment = Post.objects.create(
            author=self.author_test1,
            title="Emo Parker isn't real",
            description="He cannot hurt you",
            content="Some plaintext for Peter Parker",
            contentType="text/plain",
            visibility="PUBLIC",
            unlisted=False,
            categories=[
                "Test",
                "post",
                "author"
            ],
        )

        self.test_private_post.save()

        # Make a comment on a post
        self.test_comment1 = Comment.objects.create(
            author=self.author_test2,
            post=self.test_post_to_comment,
            comment="This is a genius movie",
            contentType="text/plain",
            post_author=self.author_test1
        )
        self.test_comment1.save()

        # Creating likes
        self.test_like1_post1 = Like.objects.create(
            author=self.author_test2,
            post=self.test_post1_author1,
        )
        self.test_like1_post1.save()

        self.test_like2_post1 = Like.objects.create(
            author=self.author_test2,
            post=self.test_post1_author1,
        )
        self.test_like2_post1.save()

        self.test_private_post_like = Like.objects.create(
            author=self.author_test2,
            post=self.test_private_post,
        )
        self.test_private_post_like.save()

        self.test_like1_post1_comment = Like.objects.create(
            author=self.author_test2,
            post=self.test_post1_author1,
            comment=self.test_comment1
        )
        self.test_like1_post1_comment.save()

    def test_like_on_post(self):
        """Testing for liking a post made by an author
            by a non-friend author
        """
        # forcing authentication of an authors
        self.client.force_authenticate(user=self.author_test1.user)
        self.client.force_authenticate(user=self.author_test2.user)

        response = self.client.get(
            reverse(
                'like_post',
                kwargs={
                    'author_id': self.author_test1.id,
                    'post_id': self.test_post1_author1.id
                }
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data[0]['summary'], 'Someone Likes your post')

    def test_like_on_comment(self):
        """Testing for liking a comment on an post made by an author
            by a non-friend author
        """
        # forcing authentication of authors
        self.client.force_authenticate(user=self.author_test1.user)

        response = self.client.get(
            reverse(
                'like_comment',
                kwargs={
                    'author_id': self.author_test1.id,
                    'post_id': self.test_post1_author1.id,
                    'comment_id': self.test_comment1.id
                }
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_like_on_private_post(self):
    #     """Testing for liking a post that is made private and can only be liked by
    #         friends of the author, being friends
    #     """
    #     # forcing authentication of authors
    #     self.client.force_authenticate(user=self.author_test1.user)
    #     self.client.force_authenticate(user=self.author_test2.user)

    #     response = self.client.get(
    #         reverse(
    #             'like_post',
    #             kwargs={
    #                 'author_id': self.author_test1.id,
    #                 'post_id': self.test_private_post.id,
    #             }
    #         )
    #     )

    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #     self.assertEqual(
    #         response.data,
    #         "It appears you are not a friend and are trying to view a friends-only posts information!"
    #     )

    def test_unsuccessful_like_on_private_post(self):
        """Testing for liking a post that is made private and can only be liked by
            friends of the author, without being friends
        """
        # forcing authentication of authors
        self.client.force_authenticate(user=self.author_test1.user)

        response = self.client.get(
            reverse(
                'like_post',
                kwargs={
                    'author_id': self.author_test1.id,
                    'post_id': self.test_private_post.id,
                }
            )
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data,
            "It appears you are not a friend and are trying to view a friends-only posts information!"
        )

    def test_author_liked_list(self):
        """
        Testing for returning a list of items of all thing an author has liked
        """
        # forcing authentication of author
        self.client.force_authenticate(user=self.author_test2.user)

        response = self.client.get(
            reverse(
                'liked_list',
                kwargs={
                    'author_id': self.author_test2.id
                }
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
