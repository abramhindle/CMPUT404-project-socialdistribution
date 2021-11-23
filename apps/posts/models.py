from django.db import models
from django.contrib.postgres.fields import ArrayField
from uuid import uuid4

from apps.core.models import Author

class Post(models.Model):
    # Enum types https://docs.djangoproject.com/en/3.2/ref/models/fields/#enumeration-types
    class VisibilityEnum(models.TextChoices):
        PUBLIC = "PUBLIC",
        FRIENDS = "FRIENDS"

    class ContentTypeEnum(models.TextChoices):
        MARKDOWN = 'text/markdown'
        PLAIN = 'text/plain'
        APPLICATION = 'application/base64'
        IMAGE_PNG = 'image/png;base64'
        IMAGE_JPEG = 'image/jpeg;base64'

    title = models.CharField(('title'), max_length=80, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    host = models.TextField(('host'))
    source = models.URLField(('source'), editable=False)
    origin = models.URLField(('origin'), editable=False)
    description = models.CharField(('description'), max_length=100, blank=True)
    contentType = models.CharField(max_length=20, choices=ContentTypeEnum.choices, default=ContentTypeEnum.PLAIN)
    content = models.TextField(('content'), max_length=280, default="")
    # author
    author = models.ForeignKey(Author, related_name='posts', on_delete=models.CASCADE)
    categories = ArrayField(models.CharField(max_length=100), default=list)
    # optional commentsSrc?
    published = models.DateTimeField(('date published'), auto_now_add=True)
    visibility = models.CharField(max_length=20, choices=VisibilityEnum.choices, default=VisibilityEnum.PUBLIC)
    unlisted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-published']

    def get_id_uri(self):
        return self.host + "/author/" + str(self.author.id) + "/posts/" + str(self.id)

    def get_comments_uri(self):
        return self.host + "/author/" + str(self.author.id) + "/posts/" + str(self.id) + "/comments/"

    def get_comments_count(self):
        return Comment.objects.filter(post=self.id).count()

    def get_source_uri(self):
        if (self.source == ""):
            return self.get_id_uri()
        else:
            return self.source

    def get_origin_uri(self):
        if (self.origin == ""):
            return self.get_id_uri()
        else:
            return self.origin

class Comment(models.Model):
    class ContentTypeEnum(models.TextChoices):
        MARKDOWN = 'text/markdown'
        PLAIN = 'text/plain'
        APPLICATION = 'application/base64'
        IMAGE_PNG = 'image/png;base64'
        IMAGE_JPEG = 'image/jpeg;base64'

    id = models.CharField(primary_key=True, default=uuid4, editable=False, unique=True, max_length=200)
    author = models.ForeignKey(Author, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    comment = models.CharField(('description'), max_length=200, blank=True)
    contentType = models.CharField(max_length=20, choices=ContentTypeEnum.choices, default=ContentTypeEnum.PLAIN)
    published = models.DateTimeField(('date published'), auto_now_add=True)

class Like(models.Model):
    summary = models.CharField(('summary'), max_length=200, blank=True)
    author = models.ForeignKey(Author, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, blank=True, null=True, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, blank=True, null=True, on_delete=models.CASCADE)

    