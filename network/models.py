from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    host = models.URLField(null=True)
    url = models.URLField(null=True)
    displayName = models.CharField(null=True, max_length=100)
    github = models.URLField(null=True)
    profileImage = models.URLField(null=True)

# https://stackoverflow.com/a/52196396 to auto-create Author when User is created
# @receiver(post_save, sender=User)
# def create_user_author(sender, instance, created, **kwargs):
#     if created:
#         Author.objects.create(user=instance)
#     instance.author.save()
