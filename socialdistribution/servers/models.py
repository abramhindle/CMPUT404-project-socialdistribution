from django.db import models
import uuid

class Server(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.URLField(max_length=1000, unique=True)
    # is_active = models.BooleanField(default=True)
