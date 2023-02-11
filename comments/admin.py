from django.contrib import admin

# Register your models here.
from .models import Comment, Comments

admin.site.register(Comment)
admin.site.register(Comments)
