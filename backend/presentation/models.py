from django.db import models
import uuid

VISIBILILTY_CHOICES = [
    ('PUBLIC', 'PUBLIC'),
    ('FRIENDS', 'FRIENDS'),
]


class Author(models.Model):
    _type = "author"
    id = models.URLField(primary_key=True, max_length=200)
    host = models.URLField(max_length=200)
    displayName = models.CharField(max_length=50)
    url = models.URLField(max_length=200)  # url to the authors profile
    github = models.URLField(max_length=200)  # HATEOS url for Github API


class Follow(models.Model):
    sender = models.URLField(max_length=200)
    receiver = models.URLField(max_length=200)
    status = models.BooleanField()


class Comment(models.Model):
    _type = "comment"
    author = models.URLField(max_length=200)
    post = models.URLField(max_length=200)
    comment = models.TextField()
    contentType = models.CharField(max_length=50)
    published = models.DateField(auto_now=False, auto_now_add=False)
    id = models.CharField(primary_key=True, max_length=200, unique=True)

    def save(self, *args, **kwargs):
        cuuid = str(uuid.uuid4().hex)
        self.id = f"{self.post}/comments/{cuuid}"
        super().save(*args, **kwargs)


class Post(models.Model):
    _type = "post"
    title = models.CharField(max_length=50)
    id = models.CharField(primary_key=True, max_length=200, unique=True)
    source = models.URLField(max_length=200)
    origin = models.URLField(max_length=200)
    description = models.CharField(max_length=200)
    contentType = models.CharField(max_length=50)
    content = models.TextField(blank=True)
    author = models.URLField(max_length=200)
    categories = models.CharField(max_length=200)  # a list of string
    count = models.IntegerField()
    size = models.IntegerField()
    comment = models.URLField(max_length=200)
    comments = models.ManyToManyField(
        Comment,
        blank=True, related_name="post_comments")  # contain Comment Objects
    published = models.DateField(
        auto_now=False, auto_now_add=False)  # ISO 8601 TIMESTAMP
    visibility = models.CharField(
        max_length=50, choices=VISIBILILTY_CHOICES, default='PUBLIC')
    # unlisted means it is public if you know the post name -- use this for images, it's so images don't show up in timelines
    unlisted = models.BooleanField()

    # https://stackoverflow.com/questions/62588857/how-can-i-create-custom-id-in-django/62588993#62588993
    def save(self, *args, **kwargs):
        puuid = str(uuid.uuid4().hex)
        self.id = f"{self.author}/posts/{puuid}"
        super().save(*args, **kwargs)


class Request(models.Model):
    _type = "Follow"
    summary = models.CharField(max_length=50)
    # send request
    actor = models.URLField(max_length=200)
    # recieve request
    object = models.URLField(max_length=200)


class Inbox(models.Model):
    _type = "inbox"
    author = models.URLField(max_length=200)
    items = models.ManyToManyField(
        Post,
        blank=True, related_name="inbox_items")  # contain Post objects


class Likes(models.Model):
    _type = "Like"
    context = models.URLField(max_length=200)  # @context?
    summary = models.CharField(max_length=50)
    author = models.URLField(max_length=200)
    object = models.URLField(max_length=200)


class Liked(models.Model):
    _type = "liked"
    items = models.ManyToManyField(
        Likes,
        blank=True, related_name="liked_items")  # contain Likes Objects
