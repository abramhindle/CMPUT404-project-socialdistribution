from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models import DateTimeField, BooleanField


# Create your models here.

# model for storing personal info of the author, linked by User model
class AuthorProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.URLField()
    displayName = models.CharField(max_length=100)
    github = models.URLField()
    bio = models.CharField(max_length=1024)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.displayName


# model for all the categories
class Category(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name


# model for a post
class Post(models.Model):
    title = models.CharField(max_length=1024)
    source = models.CharField(max_length=1024)
    origin = models.CharField(max_length=1024)
    description = models.CharField(max_length=1024)
    CONTENT_TYPE = (
        ("text/markdown", "text/markdown"),
        ("text/plain", "text/plain"),
        ("application/base64", "application/base64"),
        ("image/png;base64", "image/png;base64"),
        ("image/jpeg;base64", "image/jpeg;base64"),
    )
    contentType = models.CharField(max_length=20, choices=CONTENT_TYPE, default="text/plain")
    content = models.TextField(max_length=2 ** 21)
    author = models.ForeignKey(AuthorProfile, related_name="posts", on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    published = DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    VISIBILITY_TYPE = (
        ("PUBLIC", "PUBLIC"),
        ("FOAF", "FOAF"),
        ("FRIENDS", "FRIENDS"),
        ("PRIVATE", "PRIVATE"),
        ("SERVERONLY", "SERVERONLY"),
    )
    visibility = models.CharField(max_length=10, choices=VISIBILITY_TYPE, default="PRIVATE")
    visibleTo = models.ManyToManyField(AuthorProfile)
    unlisted = BooleanField(default=True)

    def __str__(self):
        return self.title


# model for a comment
class Comment(models.Model):
    author = models.ForeignKey(AuthorProfile, related_name="comments", on_delete=models.CASCADE)
    comment = models.TextField(max_length=2 ** 21)
    CONTENT_TYPE = (
        ("text/markdown", "text/markdown"),
        ("text/plain", "text/plain"),
        ("application/base64", "application/base64"),
        ("image/png;base64", "image/png;base64"),
        ("image/jpeg;base64", "image/jpeg;base64"),
    )
    contentType = models.CharField(max_length=20, choices=CONTENT_TYPE, default="text/plain")
    published = DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)

    def __str__(self):
        return self.id


# model for indicating the relationship between author A and author B
class Follow(models.Model):
    authorA = models.CharField(max_length=200)
    authorB = models.CharField(max_length=200)
    STATUS_TYPE = (
        ("FOLLOWING", "FOLLOWING"),
        ("FRIENDS", "FRIENDS"),
        ("DECLINED", "DECLINED"),
    )
    status = models.CharField(max_length=10, choices=STATUS_TYPE, default="FOLLOWING")

    def __str__(self):
        return self.authorA + "_" + self.authorB


