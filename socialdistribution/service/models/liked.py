from djongo import models
from service.models.likes import Likes
import uuid

# Create your models here.

class Liked(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    items = models.ManyToManyField(Likes)

    def toJSON(self):
        return {
            "type": "liked",
            "items": self.items
        }