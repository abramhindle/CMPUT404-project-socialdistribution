# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import Post

admin.site.register(User, UserAdmin)
admin.site.register(Post)
