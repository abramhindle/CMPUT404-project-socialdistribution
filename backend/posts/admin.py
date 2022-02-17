from django.contrib import admin
from .models import Post
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    ordering = ('title',)
    search_fields = ('title', 'categories', 'visibility')
    list_display = ('title', 'description', 'contentType', 'author', 'visibility')

admin.site.register(Post, PostAdmin)