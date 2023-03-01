from django.contrib import admin
from .models import Post, Comment, Friend, Inbox

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Friend)
admin.site.register(Inbox)
