# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import uuid
import json

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length = 100, default='No Title')
    source = models.CharField(max_length = 2000)
    origin = models.CharField(max_length = 2000)
    description = models.CharField(max_length =100)
    contentType_choice = (
        ('text/markdown', 'text/markdown'),
        ('text/plain', 'text/plain'),
        ('application/base64', 'application/base65'),
        ('image/png;base64', 'image/png;base64'),
        ('image/jpeg;base64', 'image/jpeg;base64'),
    )
    image = models.ImageField(null=True, blank=True)
    contentType = models.CharField(max_length=2000, choices=contentType_choice)
    content = models.TextField(max_length =10000)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    published = models.DateTimeField(default=datetime.now)#auto_now=True)
    categories = models.CharField(max_length =100, blank=True)

    visibility_choice = (
        ('PUBLIC', 'PUBLIC'),
        ('FOAF', 'FOAF'),
        ('FRIENDS', 'FRIENDS'),
        ('PRIVATE', 'PRIVATE'),
        ('SERVERONLY', 'SERVERONLY'),
    )
    visibility = models.CharField(default ="PUBLIC", max_length=20, choices=visibility_choice)
    visibleTo = models.CharField(max_length=500, blank=True)
    unlisted = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Images(models.Model):
	associated_post = models.ForeignKey(Post, on_delete=models.CASCADE)
	img = models.ImageField(null=True, blank=True)

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post_id= models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    comment =  models.TextField(max_length =2000)
    contentType_choice = (
        ('text/markdown', 'text/markdown'),
        ('text/plain', 'text/plain'),
        ('application/base64', 'application/base65'),
        ('image/png;base64', 'image/png;base64'),
        ('image/jpeg;base64', 'image/jpeg;base64'),
    )
    contentType = models.CharField(max_length=2000, default='text/plain', choices=contentType_choice)
    publi = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.author.displayName + ": " + self.comment

# Friends
class Friend(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    displayName = models.CharField(max_length=200,blank=True)
    host = models.URLField()
    url = models.URLField()
    def __str__(self):
        return self.displayName

# Profile With User
class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    host = models.URLField()
    displayName = models.CharField(max_length=200,blank=False,null=False)
    url = models.URLField()
    github = models.CharField(max_length=200,blank=True,default='')
    firstName = models.CharField(max_length=200,blank=True,default='')
    lastName = models.CharField(max_length=200,blank=True,default='')
    email = models.CharField(max_length=400,blank=True,default='')
    bio = models.CharField(max_length=2000,blank=True,default='')

    def __str__(self):  # __unicode__ for Python 2
        return self.user.username
