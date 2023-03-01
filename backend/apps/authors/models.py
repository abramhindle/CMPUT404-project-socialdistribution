from django.db import models
from django.urls import reverse
# Create your models here.


class Author(models.Model):
    id = models.BigAutoField(primary_key=True)
    url = models.URLField(max_length=200, blank=True)
    host = models.CharField(max_length=200, blank=True)
    displayName = models.CharField(max_length=200, blank=True)
    github = models.CharField(max_length=100, blank=True)
    profileImage = models.ImageField(blank=True)

    def friendlist_template():
        return {"friend_id": "[]"}
    friend_list = models.JSONField(blank=True, default=friendlist_template)

    def __str__(self):
        return self.displayName
