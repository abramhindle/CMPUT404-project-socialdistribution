from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Comment
from .serializers import CommentSerializer
from authors.models import Author
from posts.models import Post
import requests
from concurrent.futures import ThreadPoolExecutor


@receiver(post_save, sender=Comment)
def on_create_comment(sender, **kwargs):
    """This task populates the ID field with the local id of a new post"""
    if kwargs.get('created'):
        # Save The ID
        comment: Comment = kwargs.get('instance')
        url = f"{settings.DOMAIN}/authors/{comment.author.local_id}/posts/{comment.post.local_id}/comments/{comment.local_id}"
        comment.id = url

        # Save The Comment
        comment.save()
