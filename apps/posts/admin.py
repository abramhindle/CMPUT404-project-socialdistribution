from django.contrib import admin
from .models import Like, Post
from .models import Comment

# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)