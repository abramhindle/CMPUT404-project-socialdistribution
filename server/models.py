from django.db import models

class Setting(models.Model):
    allow_user_sign_up = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.pk = 1
        super(Setting, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def allow_user_sign_up(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj.allow_user_sign_up