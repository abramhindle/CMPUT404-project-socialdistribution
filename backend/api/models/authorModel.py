from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Author Model extends from Django's User model when a new account is registered
class Author(AbstractUser):
    # Author type
    type = models.CharField(default='author', max_length=100)
    # Author UUID
    uuid = models.UUIDField(primary_key=True, null=False, default=uuid.uuid4, editable=False)
    # Author URL ID
    authorID = models.URLField(null=True, blank=True)
    # Author Display Name (i.e. full name)
    displayName = models.CharField(max_length=100)
    # Author Personal URL
    url = models.URLField(null=True, blank=True)
    # Author Host URL
    host = models.URLField(max_length=150)
    # Author Github URL
    github = models.URLField(null=True, blank=True)
    # Author Profile Image
    profileImage = models.URLField(null=True, blank=True)
    # symmetrical=False allows Author to follow people that don't follow them
    followers = models.ManyToManyField("self", symmetrical=False, blank=True)
