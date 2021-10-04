from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser


# Custom user class based on Django's provided AbstractUser.
# Adds a field for storing the user's github account information.
class User(AbstractUser):
    github = models.CharField(('github'), max_length=80, blank=True)