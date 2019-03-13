# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import Post, Server
from django.contrib import admin
from preferences.admin import PreferencesAdmin
from .models import SitePreferences


admin.site.register(User, UserAdmin)
admin.site.register(Post)
admin.site.register(Server)
admin.site.register(SitePreferences, PreferencesAdmin)
