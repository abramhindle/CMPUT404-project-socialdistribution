from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class AuthorModel(models.Model):
    type = models.CharField(max_length=100, blank=False, default='author')
    id = models.CharField(max_length=100, primary_key=True)
    host = models.CharField(max_length=100, blank=False, default='')
    url = models.CharField(max_length=100, default='')
    displayName = models.CharField(max_length=100, blank=False, default='')
    github = models.CharField(max_length=100, blank=False, default='')
    profileImage = models.TextField(blank=False, default='')
    followers = ArrayField(models.CharField(max_length=100, blank=True, default=''), blank=True, default=list)
    
    class Meta:
        ordering = ['type', 'id', 'host', 'displayName', 'profileImage']

class PostsModel(models.Model):
    type = models.CharField(max_length=100, blank=False, default='post')
    title = models.CharField(max_length=100, blank=False, default='')
    id = models.CharField(max_length=100, primary_key=True)
    source = models.CharField(max_length=500, default="")
    origin = models.CharField(max_length=500, blank=False, default='')
    description = models.TextField(blank=False, default='')
    contentType = models.CharField(max_length=100, blank=False, default='')
    content = models.TextField(blank=False, default='')
    author = models.CharField(max_length=100, blank=False, default='')
    categories = ArrayField(models.CharField(max_length=100, blank=True, default=''), blank=True, default=list)
    count = models.IntegerField(default=0)
    comments = models.TextField(blank=True, default='')
    commentsSrc = ArrayField(models.CharField(max_length=100, blank=True, default=''), blank=True, default=list)
    published = models.DateTimeField(auto_now_add=True)
    visibility = models.BooleanField(default=True)
    unlisted = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['type', 'title', 'id', 'source', 'origin', 'description', 'contentType', 'content', 'author', 'categories', 'count', 'comments', 'commentsSrc', 'published', 'visibility', 'unlisted']

class CommentsModel(models.Model):
    type = models.CharField(max_length=100, blank=False, default='comment')
    author = models.CharField(max_length=100, primary_key=True)
    comment = models.TextField(blank=False, default='')
    host = models.CharField(max_length=100, blank=False, default='')
    contentType = models.CharField(max_length=100, blank=False, default='')
    published = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=500, blank=False, default='')
    post_id = models.CharField(max_length=100, blank=False, default='')
    
    class Meta:
        ordering = ['type', 'author', 'comment', 'host', 'contentType', 'published', 'id', 'post_id']

class LikeModel(models.Model):
    summary = models.CharField(max_length=200)
    type = models.CharField(max_length=100, default='like')
    author = models.CharField(max_length=255)
    object = models.CharField(max_length=255)
    class Meta:
        ordering = ['summary', 'type', 'author', 'object']