from django.contrib import admin
from post.models import Post, AuthoredPost, VisibleToAuthor

# Register your models here.
admin.site.register(Post)
admin.site.register(AuthoredPost)
admin.site.register(VisibleToAuthor)