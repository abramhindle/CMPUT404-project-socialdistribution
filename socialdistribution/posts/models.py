from django.db import models

from authors.models import AuthorId

# Create your models here.

class PostId(models.Model):
    post_id = models.IntegerField(max_length=None)
    pub_date = models.DateTimeField('date published')   

class Post(models.Model):
    VISIBILITY_CHOICE = (
        ('public','Public'),
        ('private','Private'),
    )
    title = models.CharField(max_length=200)
    categories =  models.TextField(null=True)
    description = models.CharField(max_length=200)
    visibility =  models.CharField(max_length=10, choices=VISIBILITY_CHOICE,      
    default="public")
    visibileTo =  models.TextField(null=True)

    author = models.ForeignKey(AuthorId, on_delete = models.CASCADE)
    post_id = models.ForeignKey(PostId, on_delete = models.CASCADE)


class Comment(models.Model):
    comment_id = models.IntegerField(max_length=None)
    body = models.TextField()
    pub_date = models.DateTimeField('date published')   
    post = models.ForeignKey(Post, related_name='comments', on_delete = models.CASCADE)
    author = models.ForeignKey(AuthorId, on_delete = models.CASCADE)
