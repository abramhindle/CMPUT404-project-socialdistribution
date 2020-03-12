from rest_framework.authtoken.models import Token
from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth import get_user_model

from uuid import uuid4

# Create your models here.


class Author(AbstractUser):
    # Using username, password, first_name, last_name, email from AbstractUser
    host = models.CharField(max_length=100, blank=True)
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    displayName = AbstractUser.username
    github = models.CharField(max_length=100, blank=True)
    bio = models.CharField(max_length=500, blank=True)


class Post(models.Model):
    title = models.CharField(max_length=100)
    source = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=100, blank=True)
    contentTypeChoices = [("1",'text/markdown'), ("2",'text/plain'), ("3",'application/base64'), ("4",'image/png;base64'), ("5",'image/jpeg;base64')]
    contentType = models.CharField(max_length=30, choices=contentTypeChoices)
    content = models.CharField(max_length=5000) ###TEMPORARY, how to do multiple content types?
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.CharField(max_length=100, blank=True) #### comma separated values for now?
    published = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    visibilityChoices = [("1","PUBLIC"),("2","FOAF"),("3","FRIENDS"),("4","PRIVATE"),("5","SERVERONLY")]
    visibility = models.CharField(max_length=3, choices=visibilityChoices)
    visibleTo = models.CharField(max_length=100, blank=True)
    unlisted = models.BooleanField(default=False)
    link_to_image = models.CharField(max_length=100, blank=True)


class Comment(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    contentTypeChoices = [("1",'text/markdown'), ("2",'text/plain')]
    contentType = models.CharField(max_length=30, choices=contentTypeChoices)
    published = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class FriendRequest(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid4, editable=False, unique=True)
    to_author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="to_author")
    from_author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="from_author")
    date = models.DateTimeField(auto_now_add=True)


class Follow(models.Model):
    class Meta:
        unique_together = (('follower','following'),)
    follower = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="following")
    date = models.DateTimeField(auto_now_add=True)


class Friend(models.Model):
    class Meta:
        unique_together = (('author','friend'),)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='author')
    friend = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='friend')
