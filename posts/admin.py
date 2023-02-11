from django.contrib import admin

# Register your models here.
from .models import Post, ImagePost

admin.site.register(Post)
admin.site.register(ImagePost)
