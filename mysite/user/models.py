from django.db import models
from django.contrib.auth.models import AbstractUser

DEFAULTHOST = "http://127.0.0.1:3000/"
# Create your models here.
class User(AbstractUser):
    
    email = models.EmailField(unique=True)
    host = models.URLField(default=DEFAULTHOST)
    url = models.URLField(null=True)
    github = models.URLField(null=True)
    bio = models.TextField(max_length=2048,null=True)
    is_admin = models.BooleanField(default=False)

    # Override
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


