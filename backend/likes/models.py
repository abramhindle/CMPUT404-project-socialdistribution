from django.db import models




  

class Likes(models.Model):
    type = models.CharField(max_length=100, default="Like")
    author_url = models.CharField(max_length=250, blank=False)
    summary = models.TextField(blank=False)
    context = models.URLField(blank=False, default="https://www.w3.org/ns/activitystreams")
    object= models.URLField(max_length=250, blank=False)

