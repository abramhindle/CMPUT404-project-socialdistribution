from django.db import models

VISIBILILTY_CHOICES = ["PUBLIC", "FRIENDS"]


class Author(models.Model):
    type = "author"
    id = models.URLField(max_length=200)
    host = models.URLField(max_length=200)  # the home host of the author
    # the display name of the author
    displayName = models.CharField(max_length=50)
    url = models.URLField(max_length=200)  # url to the authors profile
    github = models.URLField(max_length=200)  # HATEOS url for Github API


class Follower(models.Model):
    type = "followers"
    list = []  # contain Author Objects


class Post(models.Model):
    type = "post"
    title = models.CharField(max_length=50)
    id = models.URLField(max_length=200)
    source = models.URLField(max_length=200)
    origin = models.URLField(max_length=200)
    description = models.CharField(max_length=100)
    contentType = models.CharField(max_length=50)
    content = models.TextField()
    author = models.ForeignKey(
        "Author", on_delete=models.CASCADE, related_name="author")
    categories = []  # a list of string
    count = models.IntegerField()
    size = models.IntegerField()
    comment = models.URLField(max_length=200)
    comments = []  # contain Comment Objects
    published = models.DateField(
        auto_now=False, auto_now_add=False)  # ISO 8601 TIMESTAMP
    visibility = models.CharField(
        max_length=50, choices=VISIBILILTY_CHOICES, default="PUBLIC")
    # unlisted means it is public if you know the post name -- use this for images, it's so images don't show up in timelines
    unlisted = models.BooleanField()


class Request(models.Model):
    type = "Follow"
    summary = models.CharField(max_length=50)
    actor = models.ForeignKey(
        "Author", on_delete=models.CASCADE, related_name="author")
    object = models.ForeignKey(
        "Author", on_delete=models.CASCADE, related_name="author")


class Inbox(models.Model):
    type = "inbox"
    author = models.URLField(max_length=200)
    items = []  # contain Post objects


class Comment(models.Model):
    type = "comment"
    author = models.ForeignKey(
        "Author", on_delete=models.CASCADE, related_name="author")
    comment = models.TextField()
    contentType = models.CharField(max_length=50)
    published = models.DateField(auto_now=False, auto_now_add=False)
    id = models.URLField(max_length=200)


class Likes(models.Model):
    type = "Like"
    @context = models.URLField(max_length=200)
    summary = models.CharField(max_length=50)
    author = models.ForeignKey(
        "Author", on_delete=models.CASCADE, related_name="author")
    object = models.URLField(max_length=200)


class Liked(models.Model):
    type = "liked"
    items = []  # contain Likes Objects
