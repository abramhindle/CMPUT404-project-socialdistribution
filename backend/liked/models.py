from django.db import models
from likes.models import Likes



  

class Liked(models.Model):
    type = models.CharField(max_length=100, default="Liked")
    item = models.ForeignKey(Likes,on_delete=models.CASCADE)
