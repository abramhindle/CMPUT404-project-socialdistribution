import uuid
from django.db import models
from user.models import User
from post.models import Post

CONTENTTYPE = (
    ("text/plain", "plain text"),
    ("text/markdown", "markdown text"),
)

# Create your models here.
class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments", blank=True
    )
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments", blank=True,
    )
    content = models.CharField(max_length=400)
    contentType = models.CharField(
        max_length=16, choices=CONTENTTYPE, default="text/markdown"
    )
    published = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
