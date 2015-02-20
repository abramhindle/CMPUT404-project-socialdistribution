from django.db import models

from django.contrib.auth.models import User


class Author(models.Model):
    """Represents a author, which is a primary user in socialdistrubtion.

    Some of the things an author can do include creating and sharing posts,
    adding friends, managing their profile, and more.

    An author has a one to one relationship with Django's User, which will
    be used for login and authentication.
    """
    user = models.OneToOneField(User, primary_key=True)
