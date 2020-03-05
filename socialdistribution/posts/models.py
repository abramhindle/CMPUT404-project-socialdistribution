import uuid

from django.db import models
from PIL import Image
from profiles.models import Author


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
    description = models.CharField(max_length=200)
    categories = models.CharField(max_length=20, choices=DESCRIPTION_CHOICES,
                                  default=WEB)
    published = models.DateTimeField('date published')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES,
                                  default=PUBLIC)
    visibileTo = models.TextField(null=True )
    unlisted = models.BooleanField(default=True)
    content_type = models.CharField(max_length=20,
                                    choices=CONTENT_TYPE_CHOICES,
                                    default=PLAIN)

    image_file = models.ImageField(upload_to='media/', blank=True)



class Comment(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comment = models.TextField()
    published = models.DateTimeField('date published', auto_now_add=True)
    published.editable=True
    post = models.ForeignKey(Post, related_name='comments',
                             on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=20,
                                    choices=CONTENT_TYPE_CHOICES,
                                    default=PLAIN)
