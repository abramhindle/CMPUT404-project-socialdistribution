from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create an Author when a user is created
def createAuthor(sender, instance, created, **kwargs):
    if created:
        author, _ = Author.objects.get_or_create(user=instance)
        author.save()

post_save.connect(createAuthor, sender=User, dispatch_uid="auto_create_author")


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

    # An etag is used to retrieve events in GitHub. Normally, there is a limit
    # to the number of API calls you can make to GitHub. This limit is set to
    # 60, so it can be an issue. If we specify the etag in the header, and the
    # events haven't changed since the previous query, this won't count towards
    # our rate limit.
    github_etag = models.CharField(max_length=64, blank=True)

    def __unicode__(self):
        return self.username





    