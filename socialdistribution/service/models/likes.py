from djongo import models
from service.models.author import Author
import uuid
# Create your models here.

class Likes(models.Model):
    _id = models.ObjectIdField(auto_created=True, unique=True, primary_key=True)
    context = models.URLField()
    summary = models.CharField(max_length=50)
    type = models.CharField(max_length=4, default="like")
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    object = models.URLField()

    def toJSON(self):
        return {
            "type": "like",
            "context": self.context,
            "summary": self.summary,
            "author": self.author.toJSON(),
            "object": self.object
        }