from django.contrib import admin

from posts.models import Post, Comment
# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)