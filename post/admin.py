from django.contrib import admin
from . models import Post

# Add Post to Admin Panel
admin.site.register(Post)
