from django.db import models
from django.contrib.auth.models import AbstractUser

from .constants import CHAR_FIELD_MAX_LENGTH


class User(AbstractUser):
    github_url = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH, blank=True)
    profile_image_url = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH, blank=True)
