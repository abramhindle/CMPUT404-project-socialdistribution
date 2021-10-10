from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    id = models.ForeignKey(User, on_dlete=models.CASCADE, related_name='blog_post')
    content = models.TextField()