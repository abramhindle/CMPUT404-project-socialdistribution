from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
from .models import Post

@receiver(post_save, sender=Post)
def on_create_profile(sender, **kwargs):
    """This task populates the ID field with the local id of a new post"""
    if kwargs.get('created'):
        post: Post = kwargs.get('instance')
        print(kwargs)
        # TODO set origin and source
        post.id =f"{settings.DOMAIN}/authors/{post.author.local_id}/posts/{post.local_id}"
        post.save()
