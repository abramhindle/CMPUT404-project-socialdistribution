from django.db import models
from django.contrib.auth.models import User
import uuid
from django.conf import settings

# Create your models here.

def newId():
    return f"{settings.DOMAIN}/authors/{uuid.uuid4()}"

class Author(models.Model):
    _id = models.URLField(primary_key=True, default=newId, editable=False)
    host = models.URLField(default=settings.DOMAIN, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # link an Author to a registered user -> not required
    url = models.URLField(blank=True, null=True, unique=True)  # this is essentially the ID we get from a remote host (or just the id if its local)
    displayName = models.CharField(max_length=128)
    github = models.URLField(blank=True)
    profileImage = models.URLField(blank=True)
    followers = models.ManyToManyField('Author', blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.url:
            self.url = self._id
        super(Author, self).save(*args, **kwargs)

    def toJSON(self):
        return {
            "type": "author",
            "id": self._id,
            "host": self.host,
            "displayName": self.displayName,
            "url": self.url,
            "github": self.github,
            "profileImage": self.profileImage,
    }

    def toObject(self, json_object):
        self._id = json_object["id"]
        self.host = json_object["host"]
        self.displayName = json_object["displayName"]
        self.url = json_object["url"]
        self.github = json_object["github"]
        self.profileImage = json_object["profileImage"]

    
