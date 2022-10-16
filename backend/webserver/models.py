from django.db import models
from datetime import datetime

class Author(models.Model):
    display_name = models.CharField(max_length=200)
    profile_image = models.CharField(max_length=250)
    github_handle = models.CharField(max_length=200)

    def __str__(self):
        return self.display_name

class FollowRequest(models.Model):
    sender =  models.ForeignKey(Author, related_name='follow_requests_sent', on_delete=models.CASCADE)
    receiver =  models.ForeignKey(Author, related_name='follow_requests_received', on_delete=models.CASCADE) 

class Follow(models.Model):
    follower = models.ForeignKey(Author, related_name='following_authors', on_delete=models.CASCADE)
    followee = models.ForeignKey(Author, related_name='followed_by_authors', on_delete=models.CASCADE)

class Post(models.Model):

    author = models.ForeignKey(Author,on_delete=models.CASCADE)

    created_at = models.DateTimeField(verbose_name="date created",null=False, blank=False, default = datetime.now)

    edited_at = models.DateTimeField("date edited")

    title = models.CharField(max_length=200)

    description = models.CharField(max_length=200)

    source = models.CharField(max_length=200)

    origin = models.CharField(max_length=200)

    unlisted = models.BooleanField(default=False) 

    VISIBILITY_CHOICES = [
        ("PUBLIC","Public"),
        ("FRIENDS","Friends"),
    ]

    visibility = models.CharField(max_length=200,choices=VISIBILITY_CHOICES,default="PUBLIC")

    CONTENT_TYPE_CHOICES = [
        ("text/plain","Plain text"),
        ("text/markdown","Markdown text")
    ]

    content_type = models.CharField(max_length=200,choices=CONTENT_TYPE_CHOICES,null=False,default="text/plain")

    content = models.CharField(max_length=200)

class Comment(models.Model):
    author = models.ForeignKey(Author,on_delete=models.CASCADE)

    post = models.ForeignKey(Post,on_delete=models.CASCADE)

    content = models.CharField(max_length=200)

    created_at = models.DateTimeField("created_at")

    CONTENT_TYPE_CHOICES = [
        ("text/plain","Plain text"),
        ("text/markdown","Markdown text")
    ]

    content_type = models.CharField(max_length=200,choices=CONTENT_TYPE_CHOICES,null=False, default="text/plain")


class Like(models.Model):
    author = models.ForeignKey(Author,on_delete=models.CASCADE)

    post = models.ForeignKey(Post,on_delete=models.CASCADE)

    comment = models.ForeignKey(Comment,on_delete=models.CASCADE)