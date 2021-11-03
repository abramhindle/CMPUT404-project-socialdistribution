from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    date_created = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=200, default="Author")
    title = models.CharField(max_length=200, default="Title")
    text = models.TextField()