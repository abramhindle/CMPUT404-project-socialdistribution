from rest_framework.authtoken.models import Token
from django.db import models
from django.contrib.auth.models import AbstractUser
import social_distribution.settings as settings
import socket

from uuid import uuid4

# Create your models here.


class Node(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid4, editable=False, unique=True)
    hostname = models.URLField(
        default='127.0.0.1:8000')
    server_name = models.CharField(max_length=100)
    server_password = models.CharField(max_length=100)


class Author(AbstractUser):
    # Using username, password, first_name, last_name, email from AbstractUser
    # host = models.URLField(default=socket.gethostbyname(socket.gethostname()))
    host = models.URLField(default='127.0.0.1:8000')
    uuid = models.UUIDField(
        primary_key=True, default=uuid4, editable=False, unique=True)
    displayName = AbstractUser.username
    github = models.CharField(max_length=100, blank=True)
    bio = models.CharField(max_length=500, blank=True)

# for text fields use blank=true rather than null=true so that you don't accept None and "" as valid entries


class Post(models.Model):
    title = models.CharField(max_length=100)
    source = models.CharField(default="", max_length=100, blank=True)
    description = models.CharField(default="", max_length=100, blank=True)

    # TODO: should not give users the choice of type
    contentTypeChoices = [("1", 'text/markdown'), ("2", 'text/plain'), ("3",
                                                                        'application/base64'), ("4", 'image/png;base64'), ("5", 'image/jpeg;base64')]
    contentType = models.CharField(max_length=30, choices=contentTypeChoices)
    # TODO: TEMPORARY, how to do multiple content types?
    content = models.CharField(default="", max_length=5000, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    # TODO: comma separated values for now?
    categories = models.CharField(default="", max_length=100, blank=True)
    published = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(
        primary_key=True, default=uuid4, editable=False, unique=True)
    visibilityChoices = [("1", "PUBLIC"), ("2", "FOAF"),
                         ("3", "FRIENDS"), ("4", "PRIVATE"), ("5", "SERVERONLY")]
    visibility = models.CharField(max_length=3, choices=visibilityChoices)
    visibleTo = models.CharField(max_length=100, blank=True)
    unlistedChoices = [("1", "LISTED"), ("2", "UNLISTED")]
    unlisted = models.CharField(max_length=30, choices=unlistedChoices)

    # TODO: update url with the post id and correct path based on api
    image = models.ImageField(blank=True)
    link_to_image = models.CharField(max_length=100, blank=True)



class Comment(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid4, editable=False, unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    contentTypeChoices = [("1", 'text/markdown'), ("2", 'text/plain')]
    contentType = models.CharField(max_length=30, choices=contentTypeChoices)
    published = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class FriendRequest(models.Model):
    class Meta:
        unique_together = (('to_author', 'from_author'),)
    uuid = models.UUIDField(
        primary_key=True, default=uuid4, editable=False, unique=True)
    to_author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="to_author")
    from_author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="from_author")
    date = models.DateTimeField(auto_now_add=True)


class Follow(models.Model):
    class Meta:
        unique_together = (('follower', 'following'),)
    follower = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="following")
    date = models.DateTimeField(auto_now_add=True)


class Friend(models.Model):
    class Meta:
        unique_together = (('author', 'friend'),)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='author')
    friend = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='friend')
