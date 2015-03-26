from django.db import models


class Node(models.Model):
    """A Node represents a server that Social Distribution communicate's with.

    Social Distribution itself is a Node and will make API calls to other Nodes
    in order to send friend requests to Authors on that server. In return,
    Social Distribution will also allow other Nodes to make API requests to us.
    """
    name = models.CharField(max_length=64, blank=True)
    host = models.CharField(max_length=124, blank=True)

    def __unicode__(self):
        return '%s: %s' % (self.name, self.host)

    def get_name(self):
        return self.name

    def get_host(self):
        return self.host
