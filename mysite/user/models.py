from django.db import models
from django.contrib.auth.models import AbstractUser

DEFAULTHOST = "http://127.0.0.1:3000/"
# Create your models here.
class User(AbstractUser):
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    email = models.EmailField(unique=True)
    displayName = models.CharField(max_length=32, null=True, blank=True)
    host = models.URLField(default=DEFAULTHOST)
    github = models.URLField(null=True, blank=True)
    bio = models.TextField(max_length=2048, null=True, blank=True)

    # Override
    is_approve = models.BooleanField(default=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username
