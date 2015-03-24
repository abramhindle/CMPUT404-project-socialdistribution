from django.db import models
from time import time


class Image(models.Model):
    """Represents an image that an Author can upload."""
    thumb = models.ImageField(upload_to="static/images", blank=True, null=True)

    def __unicode__(self):
        return "image id is %d path is %s" % (self.id, self.thumb)


def get_upload_file_name(instance, filename):
    return "static/images/%s_%s" % (str(time()).replace('.', '_'), filename)
