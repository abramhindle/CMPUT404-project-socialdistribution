from djongo import models
from service.models.author import Author
from service.models.post import Post
from django.conf import settings
import uuid

def createCommentId(author_id, post_id, comment_id):
    return f"{settings.DOMAIN}/authors/{author_id}/posts/{post_id}/comments/{comment_id}"

class Comment(models.Model):
    _id = models.URLField(primary_key=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    comment = models.TextField()

    MARKDOWN = "MARKDOWN"

    CONTENT_TYPES = (
        (MARKDOWN, "text/markdown"),
    )

    contentType = models.CharField(max_length=64, choices=CONTENT_TYPES, default=MARKDOWN)
    published = models.DateTimeField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def toJSON(self, host):
        return {
            "type": "comment",
            "author": self.author.toJSON(),
            "comment": self.comment,
            "contentType": self.contentType,
            "published": str(self.published),
            "id": f"{host}authors/{self.author._id}/posts/{self.post._id}/comments/{self._id}",
        }