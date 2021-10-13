from django.contrib import admin
from .models import Author, Post, Comment, Follower

# Register your models here.
admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Follower)

