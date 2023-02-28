from djongo import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Author(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.URLField()
    user = models.OneToOneField(User, on_delete=models.CASCADE) #link an Author to a registered user
    displayName = models.CharField(max_length=128)
    github = models.URLField()
    profileImage = models.URLField()


    def toJSON(self):
        return {
            "type": "author",
            "id": str(self._id),
            "host": self.host,
            "displayName": self.displayName,
            "url": f"{self.host}/authors/{self._id}", #generated here
            "github": self.github,
            "profileImage": self.profileImage,
    }
    

