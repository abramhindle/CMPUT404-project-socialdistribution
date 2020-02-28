from rest_framework.authtoken.models import Token
from django.db import models
from django.contrib.auth.models import AbstractUser, User
import uuid

# Create your models here.


class Author(AbstractUser):
    # Using username, password from AbstractUser
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    bio = models.CharField(max_length=500, blank=True)
    github = models.CharField(max_length=100, blank=True)
    host = models.CharField(max_length=100, blank=True)


class Post(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=5000)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10)
    link_to_image = models.CharField(max_length=100)
    viewable_to = models.ManyToManyField(Author, related_name="viewable_to")


class Comment(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    body = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class FriendRequest(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    to_author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="to_author")
    from_author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="from_author")
    date = models.DateTimeField(auto_now_add=True)


class Follow(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    following = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="following")
    follower = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="follower")
    date = models.DateTimeField(auto_now_add=True)


class FriendList(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    current_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    author_friends = models.ManyToManyField(
        Author, related_name="friends_list")
