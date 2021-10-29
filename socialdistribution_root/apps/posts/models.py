from django.db import models
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
    id = models.CharField(primary_key=True, default=uuid4, editable=False, unique=True, max_length=200)
    post_id = models.CharField(default=uuid4, editable=False, unique=True, max_length=200)
    # TODO source
    # TODO origin
    description = models.CharField(('description'), max_length=200, blank=True)
    contentType = models.CharField(max_length=20, choices=ContentTypeEnum.choices, default=ContentTypeEnum.PLAIN)
    # author
    author = models.ForeignKey(Author, related_name='posts', on_delete=models.CASCADE)
    # TODO categories
    # TODO count of comments
    # TODO comments
    # optional commentsSrc? (check the forum)
    published = models.DateTimeField(('date published'), auto_now_add=True)
    visibility = models.CharField(max_length=20, choices=VisibilityEnum.choices, default=VisibilityEnum.PUBLIC)
    unlisted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-published']

    def get_post_id(self):
        return self.post_id

    def set_post_id(self, host: str):
        self.post_id = host + "/author/" + str(self.author.id) + "/posts/" + str(self.id) + "/"

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

    