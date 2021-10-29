from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from uuid import uuid4


# Custom user class based on Django's provided AbstractUser.
# Allows modifying user if needed
class User(AbstractUser):
    """
    Users within the Django authentication system are represented by this
    model.

    Username and password are required. Other fields are optional.
    """
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
    

# Create your models here.
class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    displayName = models.CharField(('displayName'), max_length=80, blank=True)
    github = models.URLField(('github'), max_length=80, blank=True)
    profileImage = models.URLField(('profileImage'), blank=True)

@receiver(post_save, sender=User)
def my_handler(sender: User, **kwargs):
    if (kwargs['created']):
        user = kwargs['instance']
        Author.objects.create(userId=user, displayName=user.username)
