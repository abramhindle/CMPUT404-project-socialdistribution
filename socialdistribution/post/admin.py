from django.contrib import admin
from post.models import Post, VisibleToAuthor, PostImage

# Register your models here.
admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(VisibleToAuthor)