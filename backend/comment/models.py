from django.db import models
import uuid
from authors.models import Author
from posts.models import Post
class Comment(models.Model):
    class ContentType(models.TextChoices):
        COMMON_MARK = "text/markdown"
        PLAIN_TEXT = "text/plain" 
    type = models.CharField(max_length=100, default="comments")
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    comment = models.TextField(blank=False)
    contentType = models.CharField(max_length=350, choices=ContentType.choices)
    published = models.DateTimeField(auto_now_add=True)
    local_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.CharField(max_length=500, default="post", blank=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
