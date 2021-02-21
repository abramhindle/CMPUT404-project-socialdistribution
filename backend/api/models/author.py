from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# NOTE: Currently none of the fields are nullable, it is up to whoever works on this to decide, best practice.
# On the Admin Page The Author Model is called Users since it is a Custom User Class.
# It automically has username and password in it
class Author(AbstractUser):
    # Note: Since this class extends the User model of django when user is created they have an ID field.
    # Therefore to get the id simply say self.id
    # User name should be handled because the User model takes first and last name
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    displayName = models.CharField(blank=True, max_length=150)
    
    # Which host this user was created on
    host    = models.URLField(max_length=500)
    
    # Full URL referencing this user
    url     = models.URLField()

    # Github Connect
    git_url = models.URLField()
