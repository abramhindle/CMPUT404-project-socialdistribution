from djongo import models
from likes import Like
from django.core import serializers

# Create your models here.

class Liked(models.Model):
    type = "Liked"
    items = models.ManyToManyField(Like,blank=True)