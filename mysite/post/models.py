import uuid
from django.db import models
from jsonfield import JSONField
from user.models import User


DEFAULTHOST = "http://127.0.0.1:3000/"

VISIBILITYCHOICES = (
    ("PUBLIC", "visible to PUBLIC"),
    ("FOAF", "visible to friends of a friend"),
    ("FRIENDS", "visiable to friends"),
    ("PRIVATE", "visiable to users listed in visiableTo field"),
    ("SERVERONLY", "visiable to a certain server"),
)
CONTENTTYPE = (
    ("text/plain", "plain text"),
    ("text/markdown", "markdown text"),
    ("image/png;base64", "png image encoding in base64"),
    ("image/jpeg;base64", "jpeg image encoding in base64"),
    ("application/base64", "application ending in base64"),
)

# Create your models here.
class Post(models.Model):
    class Meta:
        permissions = (("modify_post", "Can edit or delete the posts"),)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source = models.URLField(default=DEFAULTHOST)
    origin = models.URLField(default=DEFAULTHOST)
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=256, blank=True, default="")
    content = models.TextField()
    contentType = models.CharField(
        max_length=32, choices=CONTENTTYPE, default="text/markdown"
    )
    isImage = models.BooleanField(default=False)
    images = JSONField(null=True, blank=True)  # storing image ids.
    categories = JSONField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    published = models.DateTimeField(auto_now_add=True)
    visibility = models.CharField(
        max_length=16, choices=VISIBILITYCHOICES, default="PUBLIC"
    )
    visibleTo = JSONField(null=True, blank=True)
    unlisted = models.BooleanField(default=False)

    def __str__(self):
        return self.title
