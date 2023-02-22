from djongo import models
from service.models.author import Author
from django.core import serializers
import uuid

#Djongo freaks out if we don't define the meta values for the ArrayField CharField. This solves that problem
class Categories(models.Model):
    data = models.CharField(max_length=32)

    class Meta:
        abstract = True # is not saved as a table

class Post(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #post id
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
    #categories =  models.ArrayField(Categories, default=None) # this sucks, but we have to do it because djongo throws a hissy fit

    #dont need the comments values here, we get them at API time

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
            "id": str(self._id),
            "source": self.source,
            "origin": self.origin,
            "description": self.description,
            "contentType": self.contentType,
            "content": self.content,
            "author": self.author.toJSON(),
            "published": str(self.published),
            "visibility": self.visibility,
            "unlisted": self.unlisted
        }