import uuid
from django.db import models
from django.utils.crypto import get_random_string

def generate_password():
    return get_random_string(length=16)

class Server(models.Model):

    # https://127.0.0.1:8000
    url = models.URLField(max_length=255, unique=True)
    # https://127.0.0.1:8000/api/
    api_location = models.URLField(max_length=255, unique=True)

    # basic auth username provided by remote server
    remote_server_user = models.CharField(max_length=255)
    # basic auth password provided by remote server
    remote_server_pass = models.CharField(max_length=255)

    # basic auth username provided to remote server, default uuid4 user
    local_server_user = models.UUIDField(default=uuid.uuid4)
    # basic auth password provided to remote server, default 16 letter string
    local_server_pass = models.CharField(default=generate_password,
                                         max_length=16)

    # permissions for server
    is_active = models.BooleanField(default=True)
    share_posts = models.BooleanField(default=True)
    share_images = models.BooleanField(default=True)

    def __str__(self):
        return("%s" % (self.url))
