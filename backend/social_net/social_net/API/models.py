from django.db import models

# Create your models here.

class AuthorModel(models.Model):
    type = models.CharField(max_length=100, blank=False, default='author')
    id = models.AutoField(primary_key=True)
    host = models.CharField(max_length=100, blank=False, default='')
    displayName = models.CharField(max_length=100, blank=False, default='')
    profileImage = models.CharField(max_length=500, blank=False, default='')

    class Meta:
        ordering = ['created']
