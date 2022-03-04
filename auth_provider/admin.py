from django.contrib import admin

from .models import User
from posts.models import Post

admin.site.register(User)
admin.site.register(Post)
