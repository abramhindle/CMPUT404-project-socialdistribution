from webserver.models import Post
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
import base64

@receiver(post_save, sender=Post)
def save_image_in_binary_format(sender, instance, created, **kwargs):
    if created and instance.image:
        with open(instance.image.path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            instance.content = encoded_string
        instance.image.delete()
        instance.save()
