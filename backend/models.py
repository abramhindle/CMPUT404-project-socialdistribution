
# Create your models here.
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField
from django.db import models

import uuid


class User(AbstractUser):
    uuid = models.UUIDField(primary_key=True, uuid=uuid.uuid4, editable=False, unique=True )
    # Using: username, password, first_name, last_name, email inherited from Abstractuser

class Post(models.Model):
    postId = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title =models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=450)
    # default posts are public
    isPublic = models.BooleanField(default=True)


class PostAccess(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=CASCADE)
    accessId = models.ForeignKey(User, on_delete=CASCADE)


class Comments(models.Model):
    commentId = models.UUIDField(primary_key=True, uuid=uuid.uuid4, editable=False, unique=True)
    content = models.CharField(max_length=250)
    post = models.ForeignKey(Post, on_delete=CASCADE)
    postedBy = models.ForeignKey(User, on_delete=CASCADE)
    postedTo = models.ForeignKey(User, on_delete=CASCADE)

class FriendRequest(models.Model):
    fromUser = models.ForeignKey(User, on_delete=CASCADE)
    toUser = models.ForeignKey(User, on_delete=CASCADE)
    isAccepted = models.BooleanField(default=False)
    sentDate = models.DateTimeField(auto_now_add=True)

class Friend(models.Model):
    fromUser = models.ForeignKey(User, on_delete=CASCADE)
    toUser= models.ForeignKey(User, on_delete=CASCADE)
    friendDate = models.DateTimeField(auto_now_add=True)
    # unfriend date
    unfriendDate = models.DateTimeField(null=True, blank=True)