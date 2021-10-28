from django.contrib import admin
from .models import Setting

class SettingAdmin(admin.ModelAdmin):
    list_display = ['allow_user_sign_up']

# Register your models here.
admin.site.register(Setting, SettingAdmin)