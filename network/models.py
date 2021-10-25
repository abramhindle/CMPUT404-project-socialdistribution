from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

class Author(models.Model):
    type = models.CharField(default='author', max_length=100)
    uuid = models.UUIDField(primary_key=True, null=False, default=uuid.uuid4, editable=False)
    id = models.URLField(null=True)
    url = models.URLField(null=True)
    host = models.URLField(null=True)
    displayName = models.CharField(null=True, max_length=100)
    github = models.URLField(null=True)
    profileImage = models.URLField(null=True)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    def __init__(self, *args, **kwargs):
        super(Author, self).__init__(*args, **kwargs)
        if self.host != None:
            # make sure host ends with a '/'
            self.host += '/' if (not self.host.endswith('/')) else ''

            # set id and url to format specified in the project specifications
            self.id = self.host + self.type + '/' + str(self.uuid)
            self.url = self.id


# https://stackoverflow.com/a/52196396 to auto-create Author when User is created
# @receiver(post_save, sender=User)
# def create_user_author(sender, instance, created, **kwargs):
#     if created:
#         Author.objects.create(user=instance)
#     instance.author.save()
