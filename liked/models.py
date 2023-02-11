from django.db import models


MAX_LENGTH = 100
SMALLER_MAX_LENGTH = 50

# Create your models here.
class Liked(models.Model):
    context = models.URLField(max_length=MAX_LENGTH)
    # put in items here?