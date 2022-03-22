from django.db import models
from django.contrib.auth.models import User

class Node(models.Model):
    name = models.CharField(max_length=100, unique=True)
    host = models.URLField()
    remote_credentials = models.OneToOneField(User, on_delete=models.CASCADE)    
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
