from django.db import models


class Category(models.Model):
    name = models.TextField(unique=True)

