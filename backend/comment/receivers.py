from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment
from .serializers import CommentSerializer
import requests
import json


@receiver(post_save, sender=Comment)
def on_create_comment(sender, **kwargs):
    """This task populates the ID field with the local id of a new post"""
    if kwargs.get('created'):
        # Save The ID
        comment: Comment = kwargs.get('instance')
        comment.id = f"{comment.post.id}comments/{comment.local_id}/"

        # Push The Comment To The Recipient's Inbox
        headers = {"Content-Type": "application/json"}
        url = f"{comment.id.split('/posts/')[0]}/inbox/"
        requests.post(url=url, headers=headers, data=json.dumps(CommentSerializer(comment).data))

        # Save The Comment
        comment.save()
