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

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=1024)
    author = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)

    def __str__(self):
        return self.text
