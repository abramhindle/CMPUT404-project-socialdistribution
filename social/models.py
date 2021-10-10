from django.db import models
from django.contrib.auth.models import User

#Author class
class Author(models.Model):
    id = models.CharField(max_length=200,primary_key=True)
    host = models.CharField(max_length=200)
    displayName = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    github = models.CharField(max_length=200)

# Create your models here.
class Post(models.Model):
    #https://www.geeksforgeeks.org/how-to-use-django-field-choices/ for choices
    CONTENT_TYPES = [
        ("text/markdown", "text/markdown"),
        ("text/plain", "text/plain"),
        ("application/base64","application/base64"),
        ("image/png;base64","image/png;base64"),
        ("image/jpeg;base64","image/jpeg;base64")
    ]
    VISIBILITY = [
        ("PUBLIC", "PUBLIC"),
        ("PRIVATE", "PRIVATE")
    ]
    id = models.CharField(max_length=200,primary_key=True)
    title = models.CharField(max_length=200)
    source = models.CharField(max_length=200)
    origin = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    contentType = models.CharField(max_length=30,choices = CONTENT_TYPES)
    content = models.CharField(max_length=2000)
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    #not sure what to do for category

    #should probably be a different field type
    published = models.DateTimeField('date published')
    visibility = models.CharField(max_length=30,choices = VISIBILITY)

    #https://www.geeksforgeeks.org/booleanfield-django-models/ for boolean fields
    unlisted = models.BooleanField()
    

#means that follower follows followee
class Follower(models.Model):
    #https://stackoverflow.com/questions/2759503/django-models-use-multiple-values-as-a-key

    #https://stackoverflow.com/questions/22538563/django-reverse-accessors-for-foreign-keys-clashing
    follower = models.ForeignKey(Author, related_name='%(class)s_follower', on_delete = models.CASCADE)
    followee = models.ForeignKey(Author, related_name='%(class)s_folowee', on_delete = models.CASCADE)
    class Meta:
        unique_together = (("follower","followee"))

class Comment(models.Model):
    CONTENT_TYPES = [
        ("text/markdown", "text/markdown"),
        ("text/plain", "text/plain"),
        ("application/base64","application/base64"),
        ("image/png;base64","image/png;base64"),
        ("image/jpeg;base64","image/jpeg;base64")
    ]
    id = models.CharField(max_length=200,primary_key=True)
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    contentType = models.CharField(max_length=30,choices = CONTENT_TYPES, default= "text/plain")
    comment = models.CharField(max_length=200)
    #should probably be a different field type
    published: models.DateTimeField('date published')

#for likes on a post
class PostLike(models.Model):
    #not sure what to do for @context
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    summary = models.CharField(max_length=200)
    class Meta:
        unique_together = (("author","post"))
        
class CommentLike(models.Model):
    #not sure what to do for @context
    comment = models.ForeignKey(Comment, on_delete = models.CASCADE)
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    summary = models.CharField(max_length=200)
    class Meta:
        unique_together = (("author","comment"))
