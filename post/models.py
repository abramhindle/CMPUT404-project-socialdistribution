from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


class Post(models.Model):
    post_story = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    # Print the string representation of Post
    def __str__(self):
        return self.post_story
