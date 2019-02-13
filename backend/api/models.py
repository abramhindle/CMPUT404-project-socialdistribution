from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models import DateTimeField, BooleanField


# Create your models here.


# model for the category of a post
class PostCategory(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name


# model for a comment
class Comment(models.Model):
    author = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
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

    def __str__(self):
        return self.id


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
    author = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    categories = models.ForeignKey(PostCategory, related_name="categories", on_delete=models.PROTECT)
    comments = models.ForeignKey(Comment, related_name="comments_list", on_delete=models.CASCADE)
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
    visibleTo = models.ForeignKey(User, related_name="visible_author", on_delete=models.CASCADE)
    unlisted = BooleanField(default=True)

    def __str__(self):
        return self.title


# model for indicating the relationship between author A and author B
class Follow(models.Model):
    authorA = models.ForeignKey(User, related_name="author_A", on_delete=models.CASCADE)
    authorB = models.ForeignKey(User, related_name="author_B", on_delete=models.CASCADE)
    STATUS_TYPE = (
        ("FOLLOWING", "FOLLOWING"),
        ("FRIENDS", "FRIENDS"),
    )
    visibility = models.CharField(max_length=10, choices=STATUS_TYPE, default="FOLLOWING")

    def __str__(self):
        return self.authorA + "_" + self.authorB


# model for storing personal info of the author, linked by User model
class AuthorProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.URLField()
    displayName = models.CharField(max_length=100)
    github = models.URLField()

    def __str__(self):
        return self.id
