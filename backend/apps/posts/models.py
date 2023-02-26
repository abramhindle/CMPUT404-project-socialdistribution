from django.db import models

# Create your models here.

class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50) # change max_length later
    text = models.CharField(max_length=100) # change max_length later