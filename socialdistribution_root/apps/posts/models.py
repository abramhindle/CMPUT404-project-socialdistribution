from django.db import models
from django.http.response import HttpResponseNotAllowed
from datetime import datetime 
from uuid import uuid4

from apps.core.models import User

# Create your models here.
class Post(models.Model):
    id = models.CharField(primary_key=True, default=uuid4, editable=False, unique=True, max_length=200)
    title = models.CharField(('title'), max_length=80, blank=True)
    description = models.CharField(('description'), max_length=200, blank=True)
    # author
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    # comments
    published = models.DateTimeField(('date published'), auto_now_add=True)
    visibility = models.CharField(('visibility'), max_length=200, blank=True)

    class Meta:
        ordering = ['published']

    def get_post_id(self):
        return "http://localhost:8000/service/author/a4970609-1941-45cb-aac7-fdba50587fb0/posts/" + str(self.id) + "/"
        # return "http://" + host + "/author/" + author_id + "/posts/" + str(post_id)
    