from django.db import models

from django.contrib.auth.models import User


class Author(models.Model):
    """Represents a author, which is a primary user in socialdistribution.

    Some of the things an author can do include creating and sharing posts,
    adding friends, managing their profile, and more.

    An author has a one to one relationship with Django's User, which will
    be used for login and authentication.

    An author will also be tied to one GitHub account, which will be used to
    retrieve their GitHub feed.
    """
    user = models.OneToOneField(User, primary_key=True)
    github_user = models.CharField(max_length=128, blank=True)
