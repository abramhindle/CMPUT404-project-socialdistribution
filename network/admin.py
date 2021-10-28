from django.contrib import admin
from network import models

from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser

# Register your models here.
admin.site.register(models.Author)
admin.site.register(models.FriendRequest)
admin.site.register(models.Post)
admin.site.register(models.Comment)
admin.site.register(models.Like)

class CustomUserAdmin(UserAdmin):    
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email']

admin.site.register(CustomUser, CustomUserAdmin)
