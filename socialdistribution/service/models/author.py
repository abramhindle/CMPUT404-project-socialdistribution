from djongo import models
from django.contrib.auth.models import User
import uuid
from django.core import serializers

# Create your models here.

class Author(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.URLField()
    user = models.OneToOneField(User, on_delete=models.CASCADE) #link an Author to a registered user
    displayName = models.CharField(max_length=128)
    github = models.URLField()
    profileImage = models.URLField()

class Followers(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="all_authors")
    follower = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="all_followers")