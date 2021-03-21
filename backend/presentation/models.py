from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
import uuid
import datetime

VISIBILILTY_CHOICES = [
    ('PUBLIC', 'PUBLIC'),
    ('FRIENDS', 'FRIENDS'),
]

MAX_LENGTH = 200
MIN_LENGTH = 50


def default_list():
    return []


class Author(models.Model):
    type = "author"
    id = models.URLField(primary_key=True, max_length=MAX_LENGTH)
    host = models.URLField(max_length=MAX_LENGTH)
    displayName = models.CharField(max_length=MIN_LENGTH)
    url = models.URLField(max_length=MAX_LENGTH)  # url to the authors profile
    # HATEOS url for Github API
    github = models.URLField(max_length=MAX_LENGTH)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)


class Follower(models.Model):
    type = "followers"
    owner = models.ForeignKey(Author, on_delete=models.CASCADE)
    items = models.JSONField(default=default_list)


class Post(models.Model):
    type = "post"
    title = models.CharField(max_length=MIN_LENGTH)
    id = models.CharField(primary_key=True, max_length=MAX_LENGTH, unique=True)
    source = models.URLField(max_length=MAX_LENGTH)
    origin = models.URLField(max_length=MAX_LENGTH)
    description = models.CharField(max_length=MAX_LENGTH)
    contentType = models.CharField(max_length=MIN_LENGTH)
    content = models.TextField(blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.JSONField(default=default_list)  # a list of string
    count = models.IntegerField()
    size = models.IntegerField()
    # the first page of comments
    comments = models.URLField(max_length=MAX_LENGTH)
    published = models.DateField(
        default=datetime.date.today, auto_now=False, auto_now_add=False)  # ISO 8601 TIMESTAMP
    visibility = models.CharField(
        max_length=MIN_LENGTH, choices=VISIBILILTY_CHOICES, default='PUBLIC')
    # unlisted means it is public if you know the post name -- use this for images, it's so images don't show up in timelines
    unlisted = models.BooleanField()

    # https://stackoverflow.com/questions/62588857/how-can-i-create-custom-id-in-django/62588993#62588993
    # def save(self, *args, **kwargs):
    #    puuid = str(uuid.uuid4().hex)
    #    self.id = f"{self.author.id}/posts/{puuid}"
    #    super().save(*args, **kwargs)


class Comment(models.Model):
    type = "comment"
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    contentType = models.CharField(max_length=MIN_LENGTH)
    published = models.DateField(default=datetime.date.today, auto_now=False, auto_now_add=False)
    id = models.CharField(primary_key=True, max_length=MAX_LENGTH, unique=True)


class Request(models.Model):
    type = "follow"
    summary = models.CharField(max_length=MIN_LENGTH)
    # send request
    actor = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="request_actor")
    # recieve request
    object = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="request_object")


'''
The inbox is all the new posts from who you follow
'''


class Inbox(models.Model):
    type = "inbox"
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    items = models.JSONField(default=default_list)  # contain Post objects


class Likes(models.Model):
    type = "Like"
    context = models.CharField(max_length=MAX_LENGTH)  # @context?
    summary = models.CharField(max_length=MIN_LENGTH)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="likes_author")
    post_object = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="likes_post", null=True)
    comment_object = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="likes_comment",null=True)


class Liked(models.Model):
    type = "liked"
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    items = models.JSONField(default=default_list)  # contain Likes Objects
