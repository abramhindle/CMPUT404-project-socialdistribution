from posts.models import Post
from rest_framework.test import APITestCase, force_authenticate
from django.contrib.auth.models import User


def create_user(username):
    user = User.objects.create_user(username=username, password="test", email=f"{username}@gmail.com")
    user.is_superuser = True
    user.is_staff = True
    user.author.verified = True
    user.author.save()
    user.save()
    return user


def create_public_post(author):
    data = {"title": "Public Post Title",
            "description": "Public Post Description",
            "contentType": Post.ContentType.PLAIN_TEXT,
            "content": "Public Post Content",
            "author": author,
            "categories": ["public", "post", "test"],
            "visibility": Post.Visibility.PUBLIC,
            "unlisted": False
            }
    return Post.objects.create(**data)


def create_friend_post(author):
    data = {"title": "Friend Post Title",
            "description": "Friend Post Description",
            "contentType": Post.ContentType.PLAIN_TEXT,
            "content": "Friend Post Content",
            "author": author,
            "categories": ["friend", "post", "test"],
            "visibility": Post.Visibility.FRIENDS,
            "unlisted": False
            }
    return Post.objects.create(**data)


class InboxTests(APITestCase):

    def setUp(self) -> None:
        self.user = create_user("SuperUser")
        self.public_post = create_public_post(self.user.author)
        self.friend_post = create_friend_post(self.user.author)

    def test_get_inbox(self):
        """ Ensure we can create a new account object. """
        url = f"/api/authors/{self.user.author.local_id}/inbox/"
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        print(response.data)
        print(self.public_post)
