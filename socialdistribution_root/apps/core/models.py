from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4


# Custom user class based on Django's provided AbstractUser.
# Adds a field for storing the user's github account information.
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    displayName = models.CharField(('displayName'), max_length=80, blank=True)
    github = models.URLField(('github'), max_length=80, blank=True)
    profileImage = models.URLField(('profileImage'), blank=True)
    