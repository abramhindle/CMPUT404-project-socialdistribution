import uuid
import requests
from django.db import models
from posts.models import Post
from authors.models import Author
from django.utils.timezone import now
from posts.serializers import PostSerializer


class InboxItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(Author, on_delete=models.CASCADE)
    src = models.URLField(max_length=350)
    published = models.DateTimeField(default=now, editable=False)

    def get_post(self):
        queryset = Post.objects.filter(id=self.src)
        if len(queryset) > 0:
            return PostSerializer(queryset[0]).data
        res = requests.get(self.src)
        return res.json()
