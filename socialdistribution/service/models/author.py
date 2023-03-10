from django.db import models
from django.contrib.auth.models import User
import uuid
from django.conf import settings

# Create your models here.

def newId():
    return f"{settings.DOMAIN}/authors/{uuid.uuid4()}"

class Author(models.Model):
    _id = models.URLField(primary_key=True, default=newId, editable=False)
    host = models.URLField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True) #link an Author to a registered user -> not required
    displayName = models.CharField(max_length=128)
    github = models.URLField()
    profileImage = models.URLField()

    followers = models.ManyToManyField('Author', blank=True)

    def toJSON(self):
        return {
            "type": "author",
            "id": self._id,
            "host": self.host,
            "displayName": self.displayName,
            "url": self._id, #dont really know what this is for...
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

    
