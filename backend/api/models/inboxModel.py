from django.db import models

class Inbox(models.Model):
    # Inbox Type
    type = models.CharField(default='inbox', max_length=100)
    # Inbox Author
    author = models.URLField(null=True, blank=True)
    # Inbox Items
    items = models.JSONField(default=list, null=True, blank=True)
