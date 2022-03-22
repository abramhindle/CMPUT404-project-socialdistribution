import json

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from .models import Post
from .serializers import PostSerializer
from authors.models import Author
import requests
from requests import RequestException
import json
from inbox.models import InboxItem
from concurrent.futures import ThreadPoolExecutor
from authors.serializers import AuthorSerializer
from nodes.models import Node


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
        post.comments = url + "comments/" if not post.comments else post.comments

        # Push Posts To Recipient's Inbox
        if post.contentType != post.ContentType.PNG and post.contentType != post.ContentType.JPEG:
            data = PostSerializer(post).data
            data["author"] = AuthorSerializer(post.author).data
            if post.visibility == "PUBLIC":
                authors = Author.objects.all()
                with ThreadPoolExecutor(max_workers=1) as executor:
                    executor.map(lambda author: requests.post(f"{author.id}inbox/", json.dumps(data), headers={"Content-Type": "application/json"}), authors)
                # Push Posts to Remote Recipient's Inbox
                nodes = Node.objects.all()
                try:
                    for node in nodes:
                        with ThreadPoolExecutor(max_workers=1) as executor:
                            futures = executor.map(requests.get(f"{node.host}authors/", auth=(node.username, node.password)))
                        for future in futures:
                            remote_authors = json.loads(future.text)["items"]
                            with ThreadPoolExecutor(max_workers=1) as executor:
                                executor.map(lambda author: requests.get(f"{author['id']}inbox/", auth=(node.username, node.password)), remote_authors)
                except RequestException as e:
                    print(e)
            elif post.visibility == "FRIENDS":
                authors = Author.objects.all()
                with ThreadPoolExecutor(max_workers=1) as executor:
                    executor.map(lambda author: requests.post(f"{author.id}inbox/", json.dumps(data), headers={"Content-Type": "application/json"}), authors)
            else:
                pass

        # Save The Post
        post.save()


@receiver(post_delete, sender=Post)
def on_delete_post(sender, **kwargs):
    """WHen A Post Is Deleted, We Want To Delete All Matching Inbox Items"""
    post: Post = kwargs.get('instance')
    InboxItem.objects.filter(src=post.id).delete()

    if post.contentType == post.ContentType.COMMON_MARK:
        references = post.content.split("(")[1].split("image/)")[0]
        Post.objects.filter(id=references).delete()
