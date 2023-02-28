from django.db import models
from django.urls import reverse
# Create your models here.


class Author(models.Model):
    id = models.BigAutoField(primary_key=True)
