from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import uuid


# Create your models here.

#
# The user model is described by this specification:
# https://github.com/TeamAADGT/CMPUT404-project-socialdistribution/blob/master/example-article.json
#

# Code based on ideas by
# Nkansah Rexford (https://plus.google.com/+NkansahRexford?prsrc=5) from
# https://blog.khophi.co/extending-django-user-model-userprofile-like-a-pro/


class Node(models.Model):
    """
    Represents a local or remote server upon which remote authors and posts reside

    TODO: Add authentication
    """
    name = models.CharField(max_length=512)
    website_url = models.URLField(unique=True)
    service_url = models.URLField(unique=True)
    local = models.BooleanField(default=False)

    def __str__(self):
        return '%s (%s; %s)' % (self.name, self.website_url, self.service_url)


class Author(models.Model):
    user = models.OneToOneField(User, related_name='user')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    displayName = models.CharField(max_length=512)

    ### Optional Attributes

    # https://github.com/join
    github = models.URLField(default='', blank=True)

    bio = models.TextField(default='', blank=True)

    ### Meta Attributes
    activated = models.BooleanField(default=False)

    node = models.ForeignKey(Node, on_delete=models.CASCADE)

    def __str__(self):
        return '%s, %s (%s)' % (self.user.last_name, self.user.first_name, self.displayName)


def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if not user.is_staff and kwargs["created"]:
        user_profile = Author(user=user)
        user_profile.displayName = user_profile.user.first_name + ' ' + user_profile.user.last_name
        user_profile.save()


post_save.connect(create_profile, sender=User)

User.profile = property(lambda u: Author.objects.get_or_create(user=u)[0])
