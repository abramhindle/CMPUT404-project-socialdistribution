from django.contrib import admin
from .models import Author, Post, Comment, FriendRequest, Follow

# Register your models here.
admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(FriendRequest)
admin.site.register(Follow)
