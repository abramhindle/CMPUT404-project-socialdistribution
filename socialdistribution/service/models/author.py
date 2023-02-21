from djongo import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Author(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.URLField()
    user = models.OneToOneField(User, on_delete=models.CASCADE) #link an Author to a registered user
    displayName = models.CharField(max_length=128)
    github = models.URLField()
    profileImage = models.URLField()

    class Meta:
        permissions = [
            (
                "change_user_information",
                "Allows the user to modify their Author information"
            )
        ]