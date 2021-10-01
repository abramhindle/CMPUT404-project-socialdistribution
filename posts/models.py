import uuid
from django.db import models
from authors.models import Author
from django.utils.translation import gettext_lazy as _


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    author = models.ForeignKey(Author, related_name="commenter", on_delete=models.CASCADE)
    comment = models.TextField()
    published = models.DateTimeField()

    # TODO: question: should comments supports the same content-types as posts?
    # content_type = ?

class Post(models.Model):
    # https://docs.djangoproject.com/en/3.2/ref/models/fields/#enumeration-types
    class ContentType(models.TextChoices):
        MARKDOWN = 'MDN', _('text/markdown')
        PLAIN = 'PLN', _('text/plain')
        APPLICATION = 'APP', _('application/base64')
        IMAGE_PNG = 'PNG', _('image/png;base64')
        IMAGE_JPEG = 'JPG', _('image/jpeg;base64')

    class Visibility(models.TextChoices):
        PUBLIC = 'PUB', _('PUBLIC')
        FRIENDS = 'FRI', _('FRIENDS')
        PRIVATE = 'PRI', _('PRIVATE')

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    url = models.URLField(editable=False)
    author = models.ForeignKey(Author, related_name="post", on_delete=models.CASCADE)
    
    title = models.CharField(max_length=30) # title should not be super long
    source = models.URLField(editable=False)
    origin = models.URLField(editable=False)
    description = models.CharField(max_length = 50)
    content_type = models.CharField(max_length=3, choices=ContentType.choices, default=ContentType.PLAIN)
    content = models.TextField()
    published = models.DateTimeField()
    comments = models.ManyToManyField(Comment, related_name="post_comments", blank=True)
    unlisted = models.BooleanField(default=False)
        
    # TODO: As an author, posts I create can link to images.
    # TODO: As an author, posts I create can be images..

    # make the admin page looks pretty
    def __str__(self):
        return self.title

    # used by serializer
    def get_public_id(self):
        return self.url or self.id

    def get_api_type(self):
        return 'post'

class Like(models.Model):
    summary = models.CharField(max_length=30)
    author = models.ForeignKey(Author, related_name = "liker", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name = "liker", on_delete=models.CASCADE)

    # https://docs.djangoproject.com/en/3.2/ref/models/constraints/#django.db.models.UniqueConstraint
    class Meta:
        # ensure one author can only like a post once
        constraints = [
            models.UniqueConstraint(fields=['author', 'post'], name='unique_like')
        ]