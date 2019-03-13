from django.contrib import admin
from .models import AuthorProfile, Post, Comment, Follow
# Register your models here.
admin.site.register(AuthorProfile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Follow)
