
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
    post_id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title =models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=250)
    # default posts are public
    ispublic = models.BooleanField(default=True)


class post_access(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=CASCADE)
    accessID = models.ForeignKey(User, on_delete=CASCADE)


