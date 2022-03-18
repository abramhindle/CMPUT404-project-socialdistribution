from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Likes


@receiver(post_save, sender=Likes)
def on_create_postLikes(sender, **kwargs):
    """This task populates the ID field with the local id of a new post"""
    if kwargs.get('created'):
        # Save The ID
        likes: Likes = kwargs.get('instance')
        likes.object = f"{likes.post.id}"

        # Save The Likes
        likes.save()
