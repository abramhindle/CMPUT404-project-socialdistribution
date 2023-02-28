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
