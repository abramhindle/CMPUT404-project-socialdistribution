from djongo import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Author(models.Model):
    type = models.CharField(editable=False, null=True, max_length=6, default="author") # need this field to serialize
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.URLField()
    user = models.OneToOneField(User, on_delete=models.CASCADE) #link an Author to a registered user
    displayName = models.CharField(max_length=128)
    url = models.URLField(editable=False, null=True) # need this field to serialize
    github = models.URLField()
    profileImage = models.URLField()

    #generate url field ehre
    def save(self, *args, **kwargs):
        self.url = f"{self.host}/authors/{str(self._id)}"
        super().save(*args, **kwargs)
    
    def toJSON(self):
        return {
            "type": self.type,
            "id": str(self._id),
            "host": self.host,
            "displayName": self.displayName,
            "url": self.url,
            "github": self.github,
            "profileImage": self.profileImage,
    }