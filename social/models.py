import uuid
from django.db import models
from django.contrib.auth.models import User

#Author class
class Author(models.Model):
    # This is the UUID for the author
    id = models.UUIDField(primary_key=True, default=uuid.uuid4().hex, editable=False)
    # one2one relation with django user
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    # The URL for the home host of the author
    host = models.URLField(max_length=200)
    # The URL for the author's profile
    url = models.URLField(max_length=200)
    # The display name of the author
    displayName = models.CharField(max_length=200)
    # The followers of this author, not a bidirectional relationship 
    followers = models.ManyToManyField('self', related_name='follower', blank=True, symmetrical=False)
    # HATEOAS url for github API
    github_url = models.URLField(max_length=200)

    def __str__(self):
        return self.displayName + '-' + str(self.id)

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
        ("FOLLOWERS", "FOLLOWERS"),
        ("PRIVATE", "PRIVATE")
    ]
    # The UUID for the post
    id = models.UUIDField(primary_key=True, default=uuid.uuid4().hex, editable=False)
    # The URL for the post
    url = models.URLField(max_length=500)
    # The title of the post
    title = models.CharField(max_length=200)
    # Where did you get this post from
    source = models.URLField(max_length=200)
    # Where is it actually from
    origin = models.URLField(max_length=200)
    # A tweet length description of the post
    description = models.CharField(max_length=240)
    # The content type for the HTTP header
    contentType = models.CharField(max_length=30,choices = CONTENT_TYPES)
    # The main content of the post
    content = models.TextField(max_length=2000)

    author = models.ForeignKey(Author, on_delete = models.CASCADE, related_name='posted')
    #not sure what to do for category

    #should probably be a different field type
    published = models.DateTimeField('date published')
    visibility = models.CharField(max_length=30,choices = VISIBILITY)

    #https://www.geeksforgeeks.org/booleanfield-django-models/ for boolean fields
    unlisted = models.BooleanField(default=False)
    
class Comment(models.Model):
    CONTENT_TYPES = [
        ("text/markdown", "text/markdown"),
        ("text/plain", "text/plain"),
        ("application/base64","application/base64"),
        ("image/png;base64","image/png;base64"),
        ("image/jpeg;base64","image/jpeg;base64")
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4().hex, editable=False)
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name='comments')
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    contentType = models.CharField(max_length=30,choices = CONTENT_TYPES, default= "text/plain")
    comment = models.TextField()
    #should probably be a different field type
    published = models.DateTimeField('date published')

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
