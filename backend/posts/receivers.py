from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from .models import Post
from .serializers import PostSerializer
from authors.models import Author
import requests
from inbox.models import InboxItem
from concurrent.futures import ThreadPoolExecutor


@receiver(post_save, sender=Post)
def on_create_post(sender, **kwargs):
    """This task populates the ID field with the local id of a new post"""
    if kwargs.get('created'):
        # Save The ID
        post: Post = kwargs.get('instance')
        url = f"{settings.DOMAIN}/authors/{post.author.local_id}/posts/{post.local_id}/"
        post.id = url
        post.source = url if not post.source else post.source
        post.origin = url if not post.origin else post.origin

        # Push Posts To Recipient's Inbox
        if post.visibility == "PUBLIC":
            authors = Author.objects.all()
            with ThreadPoolExecutor(max_workers=1) as executor:
                executor.map(lambda author: requests.post(f"{author.id}inbox/", PostSerializer(post).data), authors)
        elif post.visibility == "FRIENDS":
            authors = Author.objects.all()
            with ThreadPoolExecutor(max_workers=1) as executor:
                executor.map(lambda author: requests.post(f"{author.id}inbox/", PostSerializer(post).data), authors)
        else:
            pass

        # Save The Post
        post.save()


@receiver(post_delete, sender=Post)
def on_delete_post(sender, **kwargs):
    """WHen A Post Is Deleted, We Want To Delete All Matching Inbox Items"""
    post: Post = kwargs.get('instance')
    InboxItem.objects.filter(src=post.id).delete()
