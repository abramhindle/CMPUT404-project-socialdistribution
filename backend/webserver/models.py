from unittest.util import _MAX_LENGTH
from django.db import models

class Authors(models.Model):
    display_name = models.CharField(max_length=200)
    pimage = models.ImageField()
    github_handle = models.CharField(max_length=200)

class FollowRequests(models.Model):
    sender_id =  models.ForeignKey(Authors,related_name='sender',on_delete=models.CASCADE)
    receiver_id =  models.ForeignKey(Authors,related_name='receiver',on_delete=models.CASCADE) 


class Follows(models.Model):
    follower = models.ForeignKey(Authors,related_name='follower',on_delete=models.CASCADE)
    followee = models.ForeignKey(Authors,related_name='followee',on_delete=models.CASCADE)

# Create your models here.
