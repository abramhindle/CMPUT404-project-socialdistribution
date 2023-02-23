from djongo import models
from service.models.author import Author
from service.models.post import Post
import uuid

class Comment(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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