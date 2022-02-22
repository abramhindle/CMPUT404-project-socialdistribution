from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

STR_MAX_LENGTH = 512


class Category(models.Model):
    category = models.CharField(max_length=STR_MAX_LENGTH)


class Post(models.Model):
    class ContentType(models.TextChoices):
        MARKDOWN = 'text/markdown', _('Commonmark')
        PLAIN = 'text/plain', _('Plaintext')
        BASE64 = 'application/base64', _('Base64Encoded')
        PNG = 'image/png;base64', _('PNG')
        JPG = 'image/jpeg;base64', _('JPEG')

    class Visibility(models.TextChoices):
        PUBLIC = "PUBLIC"
        FRIENDS = "FRIENDS"

    title = models.CharField(max_length=STR_MAX_LENGTH)
    description = models.CharField(max_length=STR_MAX_LENGTH)
    content_type = models.CharField(max_length=18, default=ContentType.PLAIN, choices=ContentType.choices)
    visibility = models.CharField(max_length=7, default=Visibility.PUBLIC, choices=Visibility.choices)
    content = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date_published = models.DateTimeField(auto_now_add=True)
    unlisted = models.BooleanField()
    categories = models.ManyToManyField(Category, blank=True)
