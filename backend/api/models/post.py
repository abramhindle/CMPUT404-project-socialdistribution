from django.db import models
import uuid

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    published = models.DateTimeField(auto_now_add=True)
