from django.contrib import admin
from network import models

# Register your models here.
admin.site.register(models.Author)
admin.site.register(models.FriendRequest)
admin.site.register(models.Post)
admin.site.register(models.Comment)
admin.site.register(models.Like)
