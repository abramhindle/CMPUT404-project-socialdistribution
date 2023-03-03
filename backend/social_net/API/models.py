from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class AuthorModel(models.Model):
    type = models.CharField(max_length=100, blank=False, default='author')
    id = models.CharField(max_length=100, primary_key=True)
    url = models.CharField(max_length=100, default=id)
    host = models.CharField(max_length=100, blank=False, default='')
    displayName = models.CharField(max_length=100, blank=False, default='')
    github = models.CharField(max_length=100, blank=False, default='')
    profileImage = models.CharField(max_length=500, blank=False, default='')
    followers = ArrayField(models.CharField(max_length=100, blank=True, default=''), blank=True, default=list)
    
    class Meta:
        ordering = ['type', 'id', 'host', 'displayName', 'profileImage']

class PostsModel(models.Model):
    type = models.CharField(max_length=100, blank=False, default='post')
    title = models.CharField(max_length=100, blank=False, default='')
    id = models.CharField(max_length=100, primary_key=True)
    source = models.CharField(max_length=100, default="")
    origin = models.CharField(max_length=100, blank=False, default='')
    description = models.CharField(max_length=500, blank=False, default='')
    contentType = models.CharField(max_length=100, blank=False, default='')
    content = models.CharField(max_length=500, blank=False, default='')
    author = models.CharField(max_length=100, blank=False, default='')
    categories = ArrayField(models.CharField(max_length=100, blank=True, default=''), blank=True, default=list)
    count = models.IntegerField(default=1023)
    comments = models.CharField(max_length=100, blank=False, default='')
    commentsSrc = ArrayField(models.CharField(max_length=100, blank=True, default=''), blank=True, default=list)
    published = models.DateTimeField(auto_now_add=True)
    visibility = models.BooleanField(default=True)
    unlisted = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['type', 'title', 'id', 'source', 'origin', 'description', 'contentType', 'content', 'author', 'categories', 'count', 'comments', 'commentsSrc', 'published', 'visibility', 'unlisted']
