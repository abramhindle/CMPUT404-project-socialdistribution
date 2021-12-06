from django.contrib import admin
from .models import ExternalHost, Follow, User, Author
from django.contrib.auth.admin import UserAdmin


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Author)
admin.site.register(Follow)
admin.site.register(ExternalHost)
