from djongo import models
from service.models.author import Author
import uuid

class Comment(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE) #maybe set null is better here?
    comment = models.TextField()

    MARKDOWN = "MARKDOWN"

    CONTENT_TYPES = (
        (MARKDOWN, "text/markdown"),
    )

    contentType = models.CharField(max_length=64, choices=CONTENT_TYPES, default=MARKDOWN)
    published = models.DateTimeField()
