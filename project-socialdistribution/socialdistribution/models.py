from django.db import models

# Create your models here.
class Post(models.Model):
    date_created = models.DateTimeField('date created')
    created_by = models.CharField(max_length=200, default="Author")
    title = models.CharField(max_length=200, default="Title")
    text = models.CharField(max_length=200)