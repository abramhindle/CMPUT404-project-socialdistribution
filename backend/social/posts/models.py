from django.db import models
from django.urls import reverse
from author.models import Author, Inbox
from django.contrib.contenttypes.fields import GenericRelation
from django.utils import timezone
import uuid

# Create your models here.

PUBLIC = 'PUBLIC'
PRIVATE = 'PRIVATE'
FRIENDS = 'FRIENDS'

visbility_choices = [
    (PUBLIC, 'Public'),
    (PRIVATE, 'Private'),
    (FRIENDS, 'Friends')
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
    id = models.CharField(primary_key=True, editable=False, default= uuid.uuid4, max_length=255)
    url = models.URLField(editable=False, max_length=255)  # url of post
    author = models.ForeignKey(Author, related_name="posts", on_delete=models.CASCADE)  # author of post
    categories = models.CharField(max_length=255, default="", blank=True)
    title = models.CharField(max_length=150)  # title of post
    # source = models.URLField(default="",max_length=500)  # source of post
    # origin = models.URLField(default="",max_length=500)  # origin of post
    description = models.CharField(blank=True, default="", max_length=200)  # brief description of post
    contentType = models.CharField(choices=content_types, default=PLAIN, max_length=20)  # type of content
    content = models.TextField(blank=False, default="")  # content of post
    visibility = models.CharField(choices=visbility_choices, default=PUBLIC, max_length=20)  # visibility status of post
    inbox = GenericRelation(Inbox, related_query_name='post')  # inbox in which post is in
    published = models.DateTimeField(auto_now_add=True)  # date published
    
    image = models.ImageField(null=True,blank=True)  # reference to an image in the DB

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
        return self.url or str(self.id)
    
    # get comments url
    def get_comments_source(self):
        if self.url.endswith("/"):
            return self.url + 'comments/'
        else:
            return self.url + '/comments/'
    
    def get_comment_count(self):
        return self.comments.count()

    def get_likes_count(self):
        return self.likes.count()
    
    def update_fields_with_request(self, request=None):
        if not request:
            return
        self.url = request.build_absolute_uri(self.get_absolute_url())
        self.save()

    def get_absolute_url(self):
        url = reverse('posts:detail', args=[str(self.author.id), str(self.id)])
        return url[:-1] if url.endswith('/') else url 
    
    @staticmethod
    def get_api_type():
        return 'post'

class Comment(models.Model):
    id = models.CharField(primary_key=True, editable=False, default= uuid.uuid4, max_length=255)  # ID of comment
    url = models.URLField(editable=False, max_length=500)  # URL of comment
    author = models.ForeignKey(Author, related_name = 'comments', on_delete=models.CASCADE)  # author of comment
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # post of the commen
    comment = models.TextField()  # the comment
    published = models.DateTimeField(auto_now_add=True)  # date published
    contentType = models.CharField(choices=content_types, default=PLAIN, max_length=20)  # type of content

    # get public id of comment
    def get_public_id(self):
        return self.url or self.id
    
    @staticmethod
    def get_api_type():
        return 'comment'
    
    class Meta:
        ordering = ['published']

    def __str__(self):
        return 'Comment by {}'.format(self.author)
    
class Like(models.Model):
    id = models.CharField(primary_key=True, editable=False, default= uuid.uuid4, max_length=255)  # ID of like
    summary = models.CharField (max_length=100)
    author = models.ForeignKey(Author, related_name = 'likes', on_delete=models.CASCADE)  # author of like
    object = models.URLField(max_length=500)  # URL of liked object
    inbox = GenericRelation(Inbox, related_query_name='like')  # inbox in which like is in

    # get public id of like
    def get_public_id(self):
        return self.url or self.id
    
    @staticmethod
    def get_api_type():
        return 'Like'
    
    def __str__(self):
        return 'Liked by {}'.format(self.author)
    
    ### HOW TO CONTRAINT HOW MANY TIMES AN AUTHOR LIKES AN IMAGE