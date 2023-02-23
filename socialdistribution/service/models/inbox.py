from djongo import models
from django import forms
from service.models.author import Author
from service.models.post import Post
from service.models.comment import Comment

class Inbox(models.Model):
    author = models.OneToOneField(Author, primary_key=True, on_delete=models.CASCADE)

    posts = models.ManyToManyField(Post)
    comments = models.ManyToManyField(Comment)
