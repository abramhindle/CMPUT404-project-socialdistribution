import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.timezone import now
from authors.models import Author


class Post(models.Model):
    class ContentType(models.TextChoices):
        COMMON_MARK = "text/markdown"
        PLAIN_TEXT = "text/plain"
        BASE64 = "application/base64"
        PNG = "image/png;base64"
        JPEG = "image/jpeg;base64"

    class Visibility(models.TextChoices):
        PUBLIC = "PUBLIC"
        FRIENDS = "FRIENDS"

    local_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=100, default="post")
    title = models.CharField(max_length=200)
    id = models.CharField(max_length=350, blank=True)
    source = models.URLField(max_length=350, blank=True)
    origin = models.URLField(max_length=350, blank=True)
    description = models.CharField(max_length=500, blank=True)
    contentType = models.CharField(max_length=350, choices=ContentType.choices)
    content = models.TextField()
    #target file for the image
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = ArrayField(models.CharField(max_length=100))
    published = models.DateTimeField(default=now, editable=False)
    visibility = models.CharField(max_length=100, choices=Visibility.choices)
    unlisted = models.BooleanField(default=False)
