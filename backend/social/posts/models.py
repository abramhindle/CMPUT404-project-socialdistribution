from django.db import models
from author.models import Author, Inbox
from django.contrib.contenttypes.fields import GenericRelation
from django.utils import timezone

# Create your models here.

PUBLIC = 'PUBLIC'
PRIVATE = 'PRIVATE'
FRIENDS = 'FRIENDS'

visbility_choices = [
    (PUBLIC, 'PUBLIC'),
    (PRIVATE, 'PRIVATE'),
    (FRIENDS, 'FRIENDS')
]


MARKDOWN = 'text/markdown'
PLAIN = 'text/plain'
IMAGE_PNG = 'image/png'
IMAGE_JPEG = 'image/jpeg'

content_types = [
    (MARKDOWN, 'markdown'),
    (PLAIN, 'plain'),
    (IMAGE_PNG, 'image/png;base64'),
    (IMAGE_JPEG, 'image/jpeg;base64'),
]

class Post(models.Model):
    id = models.AutoField(primary_key=True, editable=False)  # ID of post
    url = models.URLField(editable=False, max_length=500)  # url of post
    author = models.ForeignKey(Author, related_name="posts", on_delete=models.CASCADE)  # author of post
    
    title = models.CharField(max_length=200)  # title of post
    source = models.URLField(default="",max_length=500)  # source of post
    origin = models.URLField(default="",max_length=500)  # origin of post
    description = models.CharField(blank=True, default="", max_length=300)  # brief description of post
    content_type = models.CharField(choices=content_types, default=PLAIN, max_length=20)  # type of content
    content = models.TextField(blank=False, default="")  # content of post
    visibility = models.CharField(choices=visbility_choices, default=PUBLIC, max_length=20)  # visibility status of post
    inbox = GenericRelation(Inbox, related_query_name='post')  # inbox in which post is in
    published = models.DateTimeField(auto_now_add=True)  # date published
    
    refImage = models.URLField(max_length=200, default="")

    # make it pretty
    def __str__(self):
        return self.title + " (" + str(self.id) + ")"
    
    # get visbility status
    def get_visilibility(self):
        return self.Visibility(self.visibility).label

    # get content type
    def get_content_type(self):
        return self.ContentType(self.content_type).label

    # get public id of post
    def get_public_id(self):
        return self.url or self.id

    @staticmethod
    def get_api_type():
        return 'post'

class Comments(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    url = models.URLField(editable=False, max_length=500)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField(max_length=200)
    published = models.DateTimeField(auto_now_add=True)
    content_type = models.CharField(choices=content_types, default=PLAIN, max_length=20)

    @staticmethod
    def get_api_type():
        return 'comment'