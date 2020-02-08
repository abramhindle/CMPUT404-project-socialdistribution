from django.db import models

# Create your models here.

class AuthorId(models.Model):
    author_id = models.IntegerField(max_length=None)


class AuthorProfile(models.Model):
    author_id = models.ForeignKey(AuthorId, on_delete = models.CASCADE)
    author_name = models.CharField(max_length=100)
