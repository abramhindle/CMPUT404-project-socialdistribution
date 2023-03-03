from django.db import models

from django.urls import reverse
# Create your models here.


class Inbox(models.Model):
    id = models.BigAutoField(primary_key=True)
    url = models.URLField(max_length=200, blank=True)
    

    # returns lists of comments
    def commentlist_template():
        return {"comments": "[]"}
    
    def likeslist_template():
        return {"likes":"[]"}


    comment_list = models.JSONField(blank=True, default=commentlist_template)
    like_list = models.JSONField(blank=True, default=likeslist_template)
