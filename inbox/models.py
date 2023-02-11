from django.db import models

MAX_LENGTH = 100
SMALLER_MAX_LENGTH = 50


# Create your models here.
class Inbox(models.Model):
    type = models.CharField(max_length=SMALLER_MAX_LENGTH)
    author = models.URLField(max_length=MAX_LENGTH)
    # put in items (consists of posts) here?