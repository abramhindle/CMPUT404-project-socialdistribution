from django.contrib import admin

# Register your models here.
from .models import Follow, Followers

admin.site.register(Follow)
admin.site.register(Followers)

