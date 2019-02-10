from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class DummyPost(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class AuthorProfile(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    github = models.CharField(max_length=255)
    # profilePicture = models.