from django.db import models
import uuid

# Create your models here.

class Author(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.URLField()
    displayName = models.CharField(max_length=128)
    github = models.URLField()
    profileImage = models.URLField()