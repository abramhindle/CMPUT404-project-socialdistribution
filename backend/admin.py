from django.contrib import admin
from .models import Author, Comment, Like, Post, Follow, Inbox

# Register your models here.
admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Follow)
admin.site.register(Inbox)
