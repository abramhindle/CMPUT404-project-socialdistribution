from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    host = models.URLField(max_length=255)
    displayName = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    github = models.URLField(max_length=255)
    profileImage = models.URLField(max_length=255)

    def __str__(self):
        return self.displayName

class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    content = models.TextField()
    published = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.CharField(max_length=255, blank=True, null=True)
    visibility = models.CharField(max_length=255, default="PUBLIC")
    unlisted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField()
    published = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

class Like(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    object = models.URLField(max_length=255)
    published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.displayName} likes {self.object}"
