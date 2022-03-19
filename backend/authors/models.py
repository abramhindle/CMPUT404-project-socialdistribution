import uuid
from .default_profile_image import default_profile_image
from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    local_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.URLField(max_length=350)
    host = models.URLField()
    displayName = models.CharField(max_length=100, unique=True)
    github = models.URLField(max_length=350, default="", blank=True)
    profileImage = models.TextField(default=default_profile_image)
    verified = models.BooleanField(default=False)
    profile = models.OneToOneField(User, on_delete=models.CASCADE)


class Avatar(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.OneToOneField(Author, on_delete=models.CASCADE)
    content = models.TextField(default=default_profile_image)
