from django.db import models
from service.models.author import Author
import uuid
from django.conf import settings
from datetime import datetime, timezone
# Create your models here.

def get_current_date():
    datetime.now(timezone.utc)

class Like(models.Model):
    _id = models.URLField(primary_key=True)
    context = models.URLField()
    summary = models.CharField(max_length=50)
    #type = models.CharField(editable=False, null=True, max_length=4, default="like") # need this field to serialize
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    object = models.URLField()
    published = models.DateTimeField(default=get_current_date, null=True)

    def save(self, *args, **kwargs):
        self.published = datetime.now(timezone.utc)
        super(Like, self).save(*args, **kwargs)

    def toJSON(self):
        return {
            "type": "like",
            "context": self.context,
            "summary": self.summary,
            "author": self.author.toJSON(),
            "object": self.object
        }
    
    @staticmethod
    def create_like_id(author_id, post_id): #uses the last uuid value from author id, and generates a custom post_id
        author_uuid = author_id.rsplit('/', 1)[-1]
        post_uuid = post_id.rsplit('posts/', 1)[1]
        print("Lookatme", post_id)
        print(post_uuid)
        return f"{settings.DOMAIN}/authors/{author_uuid}/posts/{post_uuid}/like" #object = person being followed
    
    def __str__(self):
        return f"{self.summary}, {self._id}"