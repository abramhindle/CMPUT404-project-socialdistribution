from django.db import models

# Create your models here.

# To test djongo migration
class Person(models.Model):
    first_name = models.CharField(max_length=30)                              
    last_name = models.CharField(max_length=30)