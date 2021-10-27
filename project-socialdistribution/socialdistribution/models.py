from django.db import models

# Create your models here.
class Post(models.Model):
    date_created = models.DateTimeField('date created')
    text = models.CharField(max_length=200)