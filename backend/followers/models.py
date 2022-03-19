import uuid
from django.db import models
from authors.models import Author


class Follower(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    summary = models.CharField(max_length=200, blank=False)
    object = models.ForeignKey(Author, on_delete=models.CASCADE)
    actor = models.URLField(max_length=350, blank=False)


class Following(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    follows = models.URLField(max_length=350, blank=False)
