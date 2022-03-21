from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

from .constants import CHAR_FIELD_MAX_LENGTH


class User(AbstractUser):
    github_url = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH, blank=True)
    profile_image_url = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH, blank=True)
    is_api_user = models.BooleanField(
        default=False,
        help_text='Designates whether user has access to REST API',
        verbose_name='api access status')

    def get_absolute_url(self):
        return reverse('auth_provider:profile', kwargs={'pk': self.id})
