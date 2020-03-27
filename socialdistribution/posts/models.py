import uuid

from django.db import models
from django import forms
from PIL import Image
from profiles.models import Author
from multiselectfield import MultiSelectField
from datetime import datetime
from django.utils import timezone


MARKDOWN = 'text/markdown'
PLAIN = 'text/plain'
BASE64 = 'application/base64'
PNG = 'image/png;base64'
JPEG = 'image/jpeg;base64'

CONTENT_TYPE_CHOICES = (
    (MARKDOWN, MARKDOWN),
    (PLAIN, PLAIN),
    (BASE64, BASE64),
    (PNG, PNG),
    (JPEG, JPEG),
)


class Post(models.Model):
    PUBLIC = 'PUBLIC'
    FOAF = 'FOAF'
    FRIENDS = 'FRIENDS'
    PRIVATE = 'PRIVATE'
    SERVERONLY = 'SERVERONLY'
    WEB = "WEB"
    TUTORIAL = "TUTORIAL"

    VISIBILITY_CHOICES = (
        (PUBLIC, 'Public'),
        (FOAF, 'Friends of a friend'),
        (FRIENDS, 'Friends'),
        (PRIVATE, 'Private'),
        (SERVERONLY, 'Server only')
    )

    DESCRIPTION_CHOICES = (
        (WEB, 'Web'),
        (TUTORIAL, 'Tutorial')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.CharField(blank=True, max_length=200)
    categories = MultiSelectField(max_length=20, choices=DESCRIPTION_CHOICES,
                                  default=WEB)
    published = models.DateTimeField('date published', default=timezone.now)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES,
                                  default=PUBLIC)
    visibleTo = models.TextField(null=True, default="[]")
    unlisted = models.BooleanField(default=True)
    contentType = models.CharField(max_length=20,
                                   choices=CONTENT_TYPE_CHOICES,
                                   default=PLAIN)
    content = models.TextField(blank=True)

    @property
    def source(self):
        return("%s/posts/%s" % (self.author.host, self.id))

    @property
    def origin(self):
        return("%s/posts/%s" % (self.author.host, self.id))

    def serialize(self):

        fields = ["id", "title", "description", "categories", "published",
                  "author", "visibility", "visibleTo", "unlisted",
                  "contentType", "content"]
        post = dict()
        for field in fields:
            if field == "author":
                post["author"] = self.author.serialize()
            elif field == "published":
                post["published"] = self.published.isoformat()
            else:
                post[field] = str(getattr(self, field))

        return post


class Comment(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comment = models.TextField()
    published = models.DateTimeField('date published', auto_now_add=True)
    # published.editable=True
    post = models.ForeignKey(Post, related_name='comments',
                             on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    contentType = models.CharField(max_length=20,
                                   choices=CONTENT_TYPE_CHOICES,
                                   default=PLAIN)
