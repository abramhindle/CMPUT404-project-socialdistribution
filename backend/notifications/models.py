import uuid
from django.db import models
from authors.models import Author
from django.utils.timezone import now


class Notification(models.Model):
    class ContentType(models.TextChoices):
        FOLLOW_REQUEST = "Follow"
        COMMENT = "Comment"
        LIKE = "Like"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=100, blank=False, choices=ContentType.choices)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    actor = models.URLField(max_length=350, blank=False)
    summary = models.CharField(max_length=250, blank=False)
    published = models.DateTimeField(default=now, editable=False)
