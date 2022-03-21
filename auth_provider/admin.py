from django.contrib import admin

from .models import User
from posts.models import Post


class UserModelAdmin(admin.ModelAdmin):
    list_filter = [
        "is_api_user"
    ]


admin.site.register(User, UserModelAdmin)
admin.site.register(Post)
