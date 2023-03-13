from django.db import models
from django import forms
from service.models.author import Author
from service.models.post import Post
from service.models.comment import Comment
from service.models.follow import Follow
from service.models.like import Like

class Inbox(models.Model):
    author = models.OneToOneField(Author, primary_key=True, on_delete=models.CASCADE)

    posts = models.ManyToManyField(Post)
    comments = models.ManyToManyField(Comment)
    follow_requests = models.ManyToManyField(Follow)
    likes = models.ManyToManyField(Like)
