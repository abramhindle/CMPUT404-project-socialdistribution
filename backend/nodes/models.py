from django.db import models
from django.contrib.auth.models import User

class Node(models.Model):
    name = models.CharField(max_length=100, unique=True)
    host = models.URLField()
    credentials = models.OneToOneField(User, on_delete=models.CASCADE)
