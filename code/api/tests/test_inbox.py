# python manage.py test api

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer
import json

from socialDistribution.models import Author, Inbox

# Documentation and code samples taken from the following references:
# Django Software Foundation, https://docs.djangoproject.com/en/3.2/intro/tutorial05/
# Django Software Foundation, https://docs.djangoproject.com/en/3.2/topics/testing/overview/
# Python Software Foundation, https://docs.python.org/3/library/unittest.html


def create_author(id, username, displayName, githubUrl):
    user = mixer.blend(User, username=username)
    author = Author.objects.create(id=id, username=username, displayName=displayName, githubUrl=githubUrl, user=user)
    inbox = Inbox.objects.create(author=author)
    return author, inbox


class InboxViewTests(TestCase):

    def test_post_local_follow(self):
        author1, inbox1 = create_author(
            1,
            "user1",
            "Greg Johnson",
            "http://github.com/gjohnson"
        )
        author2, inbox2 = create_author(
            2,
            "user2",
            "Lara Croft",
            "http://github.com/laracroft"
        )

        body = {
            "type": "follow",
            "summary": "Greg wants to follow Lara",
            "actor": {
                "type": "author",
                "id": "http://127.0.0.1:8000/author/1",
                "url": "http://127.0.0.1:8000/author/1",
                "host": "http://127.0.0.1:8000/",
                "displayName": "Greg Johnson",
                "github": "http://github.com/gjohnson",
                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
            },
            "object": {
                "type": "author",
                "id": "http://127.0.0.1:8000/author/2",
                "host": "http://127.0.0.1:8000/",
                "displayName": "Lara Croft",
                "url": "http://127.0.0.1:8000/author/2",
                "github": "http://github.com/laracroft",
                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
            }
        }

        response = self.client.post(
            reverse("api:inbox", kwargs={"author_id": 2}),
            content_type="application/json",
            data=body
        )

        self.assertEqual(response.status_code, 204)

        query_set = author2.inbox.follow_requests.all()
        self.assertEqual(query_set.count(), 1)
        self.assertEqual(query_set[0], author1)
