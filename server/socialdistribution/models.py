from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    postID = models.CharField(max_length=200)
    source = models.CharField(max_length=200)
    origin = models.CharField(max_length=200)
    description = models.TextField()
    contentType = models.CharField(max_length=20)
    content = models.TextField()
    # author field
    # categories
    count = models.IntegerField()
    size = models.IntegerField()
    comments = models.CharField(max_length=200)
    # comments dict
    published = models.DateField(auto_now_add=True)
    visibility = models.CharField(max_length=10, default="PUBLIC")
    unlisted = models.BooleanField(default=False)
