from django.db import models

from django.urls import reverse
# Create your models here.


class Inbox(models.Model):
    id = models.BigAutoField(primary_key=True)
    url = models.URLField(max_length=200, blank=True)
    

    def commentlist_template():
        return {"comments": "[]"}
    
    def likeslist_template():
        return {"likes":"[]"}
    
    def followrequestlist_template():
        return {"Follow Requests": "[]"}


    comment_list = models.JSONField(blank=True, default=commentlist_template)
    like_list = models.JSONField(blank=True, default=likeslist_template)
    follow_request_list = models.JSONField(blank=True, default=followrequestlist_template)

