from django.db import models

class Setting(models.Model):
    allow_user_sign_up = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.pk = 1
        super(Setting, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def user_sign_up_enabled(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj.allow_user_sign_up

class Node(models.Model):
    # If there is a prefix it will be included in the host_url
    host_url = models.URLField()
    # The credentials we need to use to connect to the node
    authentication = models.TextField()