from django.db import models
from time import time

def get_upload_file_name(instance,filename):
	return "static/images/%s_%s" % (str(time()).replace('.','_'),filename)


# Create your models here.
class Image(models.Model):
    thumb = models.ImageField(upload_to="static/images", blank=True, null=True)

    def __unicode__(self):
        return "image id is %d", self.id
