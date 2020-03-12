from django.contrib import admin

from posts.models import Post, Comment

# Register Post and Commont model in admin.
admin.site.register(Post)
admin.site.register(Comment)