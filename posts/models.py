from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    displayName = models.CharField(max_length=200)
    github = models.URLField(blank=True)
    bio = models.CharField(max_length=256, blank=True)

    def __str(self):
        return str(self.displayName)

class Follow(models.Model):
    followee = models.ForeignKey(User, related_name='followee', on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    class Meta:
        unique_together = ('follower', 'followee')
    def __str__(self):
        return str(self.follower) + " is following " + str(self.followee)

class FollowRequest(models.Model):
    requestee = models.ForeignKey(User, related_name='requestee', on_delete=models.CASCADE)
    requester = models.ForeignKey(User, related_name='requester',on_delete=models.CASCADE)
    class Meta:
        unique_together = ('requester', 'requestee')
    def __str__(self):
        return str(self.requester) + " requested that " + str(self.requestee) + " become their friend/follower"
    
class Category(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.CharField(max_length=30, blank=True)
    def __str__(self):
        return self.category

class Post(models.Model):
    CONTENTCHOICES = (
        ("text/plain", "Plain"),
        ("text/markdown", "Markdown"),
        ("application/base64", "Base64"),
        ("img/png;base64", "PNG"),
        ("image/jpeg;base64", "JPEG")
    )

    VISIBILITY = (
        ("PUBLIC", "Public"),
        ("PRIVATE", "Private"),
        ("FOAF", "Friend of a Friend"),
        ("FRIENDS", "Friends"),
        ("SERVERONLY", "Server Only")
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    source = models.URLField(blank=True)
    origin = models.URLField(blank=True)
    description = models.CharField(max_length=400)
    contentType = models.CharField(max_length=18, choices=CONTENTCHOICES, default="text/plain")
    content = models.TextField()
    published = models.DateTimeField(auto_now_add=True)
    visibility = models.CharField(max_length=7, choices=VISIBILITY, default="PUBLIC")
    unlisted = models.BooleanField(default=False)

    # # TODO: missing visibleTo
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, blank=True)

class Comment(models.Model):

    PLAIN = "text/plain"
    CONTENTCHOICES = (
        ("text/plain", "Plain"),
        ("text/markdown", "Markdown")
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent_post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    # TODO: Check if max_len=400 is fine
    comment = models.CharField(max_length=400)
    contentType = models.CharField(max_length=18, choices=CONTENTCHOICES, default=PLAIN)
    # ISO 8601 TIMESTAMP
    published = models.DateTimeField(auto_now_add=True)
