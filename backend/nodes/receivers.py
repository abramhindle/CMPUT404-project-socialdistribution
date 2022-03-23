from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from nodes.models import Node


@receiver(post_save, sender=Node)
def on_create_node(sender, **kwargs):
    """This task creates a corresponding user object whenever a new node is created"""
    if kwargs.get('created'):
        node: Node = kwargs.get('instance')
        user = User.objects.create_user(username=node.username, password=node.password)
        user.set_password(node.password)
        user.save()
        node.remote_credentials = user
        node.save()


@receiver(post_delete, sender=Node)
def on_delete_node(sender, **kwargs):
    node: Node = kwargs.get('instance')
    node.remote_credentials.delete()
