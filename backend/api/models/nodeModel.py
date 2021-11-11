from django.db import models

# Node Model
class Node(models.Model):  
    # Host URL (Main identifier for hosts)
    host = models.URLField(max_length=200)
    # Host displayName[username] for (Basic Authentication)
    displayName = models.CharField(max_length=100, null=False)
    # Host password for (Basic Authentication)
    password = models.CharField(max_length=128, verbose_name='password', null=False)
    # Host connected date
    connectedDate = models.DateTimeField(auto_now_add=True)

    def __init__(self, *args, **kwargs):
        super(Node, self).__init__(*args, **kwargs)
        if self.host != None:
            # make sure host ends with a '/'
            self.host += '/' if (not self.host.endswith('/')) else ''
        return (f"Node: Host={self.host}, Name={self.displayName}, Password={self.password}")