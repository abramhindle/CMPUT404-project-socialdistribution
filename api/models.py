import os
from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid
from .utils import create_author_url, build_url, create_post_url, create_comment_url
from django.contrib.auth.models import User


class NodeModel(models.Model):
    node_url = models.URLField()
    node_name = models.CharField(max_length=25, default='anonymous node')
    node_user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Note: we're team 16... this is our credentials to their node.
    t16_uname = models.CharField(max_length=25)
    t16_pw = models.CharField(max_length=25)
    class Meta:
        ordering = ('node_url',)


class AuthorModel(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.URLField(default='', unique=True)

    type = models.CharField(max_length=100, blank=False, default='author')
    host = models.URLField(blank=False, default='')
    url = models.URLField(default='')
    displayName = models.CharField(max_length=100, blank=False, default='')
    github = models.URLField(blank=False, default='')
    profileImage = models.TextField(blank=False, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        author_url = create_author_url()
        ## check if self.id is empty or non uuid
        
        if not self.id:
            self.id = author_url
            self.url = author_url
        if not self.host:
            self.host = build_url()
        
        super(AuthorModel, self).save(*args, **kwargs)

    class Meta:
        ordering = ('created_at',)
        
        


class PostsModel(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.URLField(default='', unique=True)
    type = models.CharField(max_length=100, blank=False, default='post')
    title = models.CharField(max_length=100, blank=False, default='')
    source = models.URLField(default=os.getenv('HOST', 'http://localhost:8000')+'/service/author/posts')
    origin = models.URLField(blank=False, default=os.getenv('HOST', 'http://localhost:8000')+'/service/author/posts')
    description = models.TextField(blank=False, default='')
    contentType = models.CharField(max_length=100, blank=False, default='')
    content = models.TextField(blank=False, default='')
    categories = ArrayField(models.CharField(max_length=100, blank=True, default=''), blank=True, default=list)
    count = models.IntegerField(default=0)
    published = models.DateTimeField(auto_now_add=True)

    class Visibility(models.TextChoices):
        PUBLIC = 'PUBLIC'
        PRIVATE = 'PRIVATE'
        UNLISTED = 'UNLISTED'

    visibility = models.CharField(max_length=100,choices=Visibility.choices,default=Visibility.PUBLIC,)
    unlisted = models.BooleanField(default=False)
    ## foreign keys
    author = models.ForeignKey('AuthorModel', on_delete=models.CASCADE, to_field='id', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            post_url = create_post_url(self.author.id)
            self.id = post_url
        super(PostsModel, self).save(*args, **kwargs)

    class Meta:
        ordering = ('published', )


class ImageModel(models.Model):
    url_id = models.URLField(default='')
    post = models.OneToOneField('PostsModel',  on_delete=models.CASCADE, to_field='id', blank=True, null=True)
    author = models.OneToOneField('AuthorModel', on_delete=models.CASCADE, to_field='id', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/')


class CommentsModel(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.URLField(default='', unique=True)

    type = models.CharField(max_length=100, blank=False, default='comment')
    author = models.ForeignKey('AuthorModel', on_delete=models.CASCADE, to_field='id', blank=True, null=True)
    comment = models.TextField(blank=False, default='')
    host = models.URLField(blank=False, default='')
    contentType = models.CharField(max_length=100, blank=False, default='')
    published = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('PostsModel', on_delete=models.CASCADE, to_field='id', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        comment_url = create_comment_url(self.post.id)
        self.id = comment_url
        super(CommentsModel, self).save(*args, **kwargs)

    class Meta:
        ordering = ('created_at',)

class LikeModel(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, unique=True)

    summary = models.TextField(blank=False, default='')
    type = models.CharField(max_length=100, default='like')
    author = models.ForeignKey('AuthorModel', on_delete=models.CASCADE, null=True, blank=True, to_field='id')
    object = models.URLField(default='')
    post = models.ForeignKey('PostsModel', on_delete=models.CASCADE, null=True, blank=True, to_field='id')
    comment = models.ForeignKey('CommentsModel', on_delete=models.CASCADE, null=True, blank=True, to_field='id')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.post:
            self.object = self.post.id
        elif self.comment:
            self.object = self.comment.id
        super(LikeModel, self).save(*args, **kwargs)

    class Meta:
        ordering = ('created_at',)


class FollowModel(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, unique=True)

    class Status(models.TextChoices):
        PENDING = 'pending'
        FRIENDS = 'friends'
        NOT_FRIENDS = 'not_friends'

    type = models.CharField(max_length=100, blank=False, default='follow')
    status = models.CharField(max_length=100, choices=Status.choices, default=Status.NOT_FRIENDS)
    following = models.TextField(blank=False, default='')
    follower = models.TextField(blank=False, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)
    

class InboxModel(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, unique=True)      # I'm guessing this must be to avoid uuid clashes when receiving content from multiple servers

    class InboxType(models.TextChoices):
        POST = 'post'
        COMMENT = 'comment'
        FOLLOW = 'follow'
        LIKE = 'like'

    type = models.CharField(max_length=100, choices=InboxType.choices, default=InboxType.POST)
    author = models.ForeignKey('AuthorModel', on_delete=models.CASCADE, null=True, blank=True, to_field='id')
    ## We will store what we receive in the inbox as a JSON object.
    object = models.JSONField(blank=False, default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)