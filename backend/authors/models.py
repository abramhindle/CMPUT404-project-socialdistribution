import uuid
from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    local_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.URLField(max_length=350)
    host = models.URLField()
    displayName = models.CharField(max_length=100)
    github = models.URLField(max_length=350, default="")
    profileImage = models.URLField(max_length=350, default="https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_1280.png")
    profile = models.OneToOneField(User, on_delete=models.CASCADE)

