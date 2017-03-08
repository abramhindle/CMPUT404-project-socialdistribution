from django.contrib import admin

# Register your models here.
from dashboard.models import UserProfile

admin.site.register(UserProfile)
