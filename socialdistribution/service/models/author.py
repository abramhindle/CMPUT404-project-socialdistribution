from djongo import models
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


    def toJSON(self):
        return {
            "type": "author",
            "id": self._id,
            "host": self.host,
            "displayName": self.displayName,
            "url": f"{self.host}/authors/{self._id}", #generated here
            "github": self.github,
            "profileImage": self.profileImage,
    }