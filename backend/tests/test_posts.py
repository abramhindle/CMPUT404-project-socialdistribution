from backend.apis import *
from backend.models import *

from django.urls import reverse
from django.contrib.auth import authenticate, login

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

USER_LOGIN_URL = reverse('author_login')


class TestPostViewSet(APITestCase):
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
            github="https://www.github.com/jonSnow"
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

        self.test_post2_author1 = Post.objects.create(
            author=self.author_test1,
            title="The Nights Watch",
            description="Jon Snow on being a member",
            content="Some plaintext for Aarya",
            contentType="text/plain",
            visibility="PUBLIC",
            unlisted=False,
            categories=[
                "Test",
                "post",
                "author"
            ],
        )

        self.test_post2_author1.save()

        self.test_post_todelete = Post.objects.create(
            author=self.author_test2,
            title="The Golden Company",
            description="Blackfyres FTW",
            content="Some plaintext for Bittersteel",
            contentType="text/plain",
            visibility="PUBLIC",
            unlisted=False,
            categories=[
                "Test",
                "post",
                "author"
            ],
        )

        self.test_post_todelete.save()

        self.test_post_to_putupdate = Post.objects.create(
            author=self.author_test2,
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

        self.test_post_to_putupdate.save()

    def test_create_post(self):
        """Testing for creation of a post made by an author
        """
        # forcing authentication of an author
        self.client.force_authenticate(user=self.author_test1.user)

        # Payload for creating a post
        create_request = {
            "type": "post",
            "title": "This is the third best post of all time",
            "description": "this is a text post",
            "contentType": "text/plain",
            "content": "This is some text that goes in the post body",
            "categories": [
                "Test",
                "post",
                "author"
            ],
            "visibility": "PUBLIC",
            "unlisted": False,
            "author": {
                "type": "author",
                "id": "http://localhost:8000/author/{}".format(self.author_test1.id),
                "host": "http://localhost:8000/",
                "displayName": "Jon Snow",
                "github": "https://www.github.com/jonSnow"
            }
        }

        response = self.client.post(
            reverse(
                'posts_object',
                kwargs={
                    'author_id': self.author_test1.id
                }
            ),
            create_request,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn('type', response.data)
        self.assertIn('title', response.data)
        self.assertIn('id', response.data)
        self.assertIn('source', response.data)
        self.assertIn('origin', response.data)
        self.assertIn('description', response.data)
        self.assertIn('contentType', response.data)
        self.assertIn('content', response.data)
        self.assertIn('author', response.data)
        self.assertIn('categories', response.data)
        self.assertIn('count', response.data)
        self.assertIn('unlisted', response.data)
        self.assertIn('published', response.data)
        self.assertIn('comments', response.data)
        self.assertIn('visibility', response.data)

    def test_incorrect_author(self):
        """Testing for creating post using different author
        """
        # forcing authentication of an author
        self.client.force_authenticate(user=self.author_test2.user)

        create_request = {
            "type": "post",
            "title": "",
            "description": "this is a bad text post",
            "contentType": "text/plain",
            "author": {
                "type": "author",
                "id": "http://localhost:8000/author/{}".format(self.author_test2.id),
                "host": "http://localhost:8000/",
                "displayName": "Arya Stark",
                "github": "https://www.github.com/AryaStark"
            }
        }

        response = self.client.post(
            reverse(
                'posts_object',
                kwargs={
                    'author_id': self.author_test1.id
                }
            ),
            create_request,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_post_list(self):
        """Testing for returning a list of all public posts made by author
        """
        # forcing authentication of an author
        self.client.force_authenticate(user=self.author_test1.user)

        list_response = self.client.get(
            reverse('posts_object', kwargs={'author_id': self.author_test1.id}))

        self.assertEqual(list_response.status_code, status.HTTP_200_OK)

    def test_get_author_post(self):
        """Testing for retrieving a post made by an author
        """
        # forcing authentication of an author
        self.client.force_authenticate(user=self.author_test1.user)

        response = self.client.get(
            reverse(
                'post_object',
                kwargs={'author_id': self.author_test1.id, 'id': self.test_post1_author1.id})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["title"], 'I dun wannit')
        self.assertEqual(response.data["author"]['displayName'], 'Jon Snow')

    def test_update_author_post(self):
        """Testing for updating a post made by an author
        """
        # forcing authentication of an author
        self.client.force_authenticate(user=self.author_test1.user)

        update_request = {
            "title": "My name is now Jahaerys",
            "description": "This is the coolest thing ever",
            "source": "http://localhost:8000/",
            "origin": "http://localhost:8000/",
            "content": "This is the updated content",
            "contentType": "text/plain",
            "categories": [
                "Test",
                "post",
                "author"
            ],
            "visibility": "PUBLIC",
            "unlisted": False,
            "author": {
                "type": "author",
                "id": "http://localhost:8000/author/{}".format(self.author_test1.id),
                "host": "http://localhost:8000/",
                "displayName": "Jon Snow",
                "github": "https://www.github.com/jonSnow"
            }
        }

        response = self.client.post(
            reverse(
                'post_object',
                kwargs={'author_id': self.author_test1.id,
                        'id': self.test_post1_author1.id
                        }
            ),
            update_request,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["title"], 'My name is now Jahaerys')
        self.assertEqual(response.data["description"],
                         'This is the coolest thing ever')
        self.assertEqual(response.data["author"]['displayName'], 'Jon Snow')

    def test_update_author_post(self):
        """Testing for incorrectly updating a post made by an author
        """
        update_request = {
            "description": "This is the coolest thing ever",
            "contentType": "text/plain",
            "content": "This is some text that goes in the post body to update",
            "categories": [
                "Test",
                "post",
                "author"
            ],
            "visibility": "PUBLIC",
            "unlisted": False,
            "author": {
                "type": "author",
                "id": "http://localhost:8000/author/{}".format(self.author_test1.id),
                "host": "http://localhost:8000/",
                "displayName": "Jon Snow",
                "github": "https://www.github.com/jonSnow"
            }
        }

        # forcing authentication of an author
        self.client.force_authenticate(user=self.author_test1.user)

        response = self.client.post(
            reverse(
                'post_object',
                kwargs={'author_id': self.author_test1.id, 'id': self.test_post1_author1.id}),
            update_request,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_author_post(self):
        """Testing for deleting a post made by an author
        """
        # forcing authentication of an author
        self.client.force_authenticate(user=self.author_test2.user)

        delete_response = self.client.delete(
            reverse(
                'post_object',
                kwargs={'author_id': self.author_test2.id,
                        'id': self.test_post_todelete.id}
            )
        )

        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)

    def test_create_specific_author_post(self):
        """Testing for creating a post given author and specific post id (PUT)
        """
        post_id = self.test_post_to_putupdate.id

        # forcing authentication of an author
        self.client.force_authenticate(user=self.author_test2.user)
        put_request = {
            "title": "National Treasure",
            "id": "http://localhost:8000/author/{}/posts/{}".format(
                self.author_test2.id, post_id
            ),
            "description": "Benny Franklin",
            "source": "http://localhost:8000/",
            "origin": "http://localhost:8000/",
            "content": "Some plaintext for Washington",
            "contentType": "text/plain",
            "categories": [
                "Test",
                "post",
                "author"
            ],
            "visibility": "PUBLIC",
            "unlisted": False,
            "author": {
                "type": "author",
                "id": "http://localhost:8000/author/{}".format(self.author_test2.id),
                "host": "http://localhost:8000/",
                "displayName": "Arya Stark",
                "github": "https://www.github.com/aryastark"
            }
        }

        response = self.client.put(
            reverse(
                'post_object',
                kwargs={'author_id': self.author_test2.id,
                        'id': post_id
                        }
            ),
            put_request,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
