from rest_framework.authtoken.models import Token
from django.db import models
from django.contrib.auth.models import AbstractUser, User
import uuid

# Create your models here.


class Author(AbstractUser):
    # Using username, password from AbstractUser
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    stream = models.CharField(max_length=500)
    # Still need to add relationships between users


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=5000)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10)
    link_to_image = models.CharField(max_length=100)


class Comment(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    body = models.CharField(max_length=5000)
    date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
