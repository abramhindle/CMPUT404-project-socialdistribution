from django.contrib import admin
from .models import Comment, Like, Post

# Register your models here.
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Post)