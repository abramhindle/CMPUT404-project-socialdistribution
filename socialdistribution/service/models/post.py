from djongo import models
from django import forms
from service.models.author import Author
import uuid
from django.conf import settings

#Djongo freaks out if we don't define the meta values for the ArrayField CharField. This solves that problem
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

    published = models.DateTimeField()

    PUBLIC = "PUBLIC"
    FRIENDS = "FRIENDS"

    VISIBILITY_CHOICES = (
        (PUBLIC, "PUBLIC"),
        (FRIENDS, "FRIENDS")
    )

    visibility = models.CharField(max_length=7, choices=VISIBILITY_CHOICES)
    unlisted = models.BooleanField(default=False)

    def toJSON(self, comments=list):
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


def createPostId(author_id, post_id):
    return f"{settings.DOMAIN}/authors/{author_id}/posts/{post_id}"
