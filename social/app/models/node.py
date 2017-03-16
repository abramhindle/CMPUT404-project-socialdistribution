from django.db import models


class Node(models.Model):
    """
    Represents a local or remote server upon which remote authors and posts reside

    TODO: Add authentication
    """
    name = models.CharField(max_length=512)
    host = models.URLField(unique=True)
    service_url = models.URLField(unique=True)
    local = models.BooleanField(default=False)

    def __str__(self):
        return '%s (%s; %s)' % (self.name, self.host, self.service_url)
