from django.db import models
from django import forms
from service.models.author import Author
import uuid
from datetime import datetime, timezone
from django.conf import settings

def get_current_date():
    datetime.now(timezone.utc)

class Category(models.Model):
    data = models.CharField(max_length=32, primary_key=True)

class Post(models.Model):
    _id = models.URLField(primary_key=True) #post id
    title = models.CharField(max_length=32)
    source = models.URLField()
    origin = models.URLField()
    description = models.TextField()

    MARKDOWN = "text/markdown"
    PLAIN = "text/plain"
    BASE64 = "application/base64"
    IMAGE_PNG = "image/png"
    IMAGE_JPEG = "image/jpeg"

    CONTENT_TYPES = (
        (MARKDOWN, "text/markdown"),
        (PLAIN, "text/plain"),
        (BASE64, "application/base64"),
        (IMAGE_PNG, "image/png"),
        (IMAGE_JPEG, "image/jpeg")
    )

    contentType = models.CharField(max_length=20, choices=CONTENT_TYPES, default=MARKDOWN)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    categories = models.ManyToManyField(Category)

    published = models.DateTimeField(default=get_current_date)

    PUBLIC = "PUBLIC"
    FRIENDS = "FRIENDS"

    VISIBILITY_CHOICES = (
        (PUBLIC, "PUBLIC"),
        (FRIENDS, "FRIENDS")
    )

    visibility = models.CharField(max_length=7, choices=VISIBILITY_CHOICES)
    unlisted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.published = datetime.now(timezone.utc)
        super(Post, self).save(*args, **kwargs)

    def toJSON(self):
        return {
            "type": "post",
            "title": self.title,
            "id": self._id,
            "source": self.source,
            "origin": self.origin,
            "description": self.description,
            "contentType": self.contentType,
            "content": self.content,
            "author": self.author.toJSON(),
            "categories": list(self.categories.values_list(flat=True)),
            "published": str(self.published),
            "visibility": self.visibility,
            "unlisted": self.unlisted
        }

    def toObject(self, json_object):
        self._id = json_object["id"] #this is a url, we need to get the last item of the url
        self.title = json_object["title"]
        self.id = json_object["id"]
        self.source = json_object["source"]
        self.origin = json_object["origin"]
        self.description = json_object["description"]
        self.contentType = json_object["contentType"]
        self.content = json_object["content"]
        self.author = Author().toObject(json_object["author"])
        self.categories = json_object["categories"]
        self.comments = json_object["comments"]
        self.published = json_object["published"]
        self.visibility = json_object["visibility"]
        self.unlisted = bool(json_object["unlisted"])

    @staticmethod
    def create_post_id(author_id, post_id=None): #uses the last uuid value from author id, and generates a custom post_id
        if not post_id:
            post_id = uuid.uuid4()

        author_uuid = author_id.rsplit('/', 1)[-1]
        return f"{settings.DOMAIN}/authors/{author_uuid}/posts/{post_id}"

    def __str__(self):
        return f"{self.title}, {self.author}, {self.published}"

