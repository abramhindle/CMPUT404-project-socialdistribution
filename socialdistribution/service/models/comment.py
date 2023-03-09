from django.db import models
from service.models.author import Author
from service.models.post import Post
from django.conf import settings
import uuid

class Comment(models.Model):
    _id = models.URLField(primary_key=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    comment = models.TextField()

    MARKDOWN = "MARKDOWN"
    PLAIN = "text/plain"


    CONTENT_TYPES = (
        (MARKDOWN, "text/markdown"),
        (PLAIN, "text/plain"),
    )

    contentType = models.CharField(max_length=64, choices=CONTENT_TYPES, default=MARKDOWN)
    published = models.DateTimeField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def toJSON(self):
        return {
            "type": "comment",
            "author": self.author.toJSON(),
            "comment": self.comment,
            "contentType": self.contentType,
            "published": str(self.published),
            "id": self._id, 
        }
    
    def toObject(self, json_object):
        self.author = Author().toObject(json_object["author"])
        self.comment = json_object["comment"]
        self.contentType = json_object["contentType"]
        self.published = json_object["published"]
        self._id = json_object["id"]

    @staticmethod
    def create_comment_id(author_id, post_id, comment_id=None):
        if not comment_id:
            comment_id = uuid.uuid4()

        author_uuid = author_id.rsplit('/', 1)[-1]
        post_uuid = post_id.rsplit('/', 1)[-1]
        return f"{settings.DOMAIN}/authors/{author_uuid}/posts/{post_uuid}/comments/{comment_id}" #TODO: rather than the whole id, just get the ends of _id and put those here
