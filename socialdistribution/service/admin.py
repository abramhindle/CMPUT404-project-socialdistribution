from django.contrib import admin
from service.models import author, posts


# Register your models here.

admin.site.register(author.Author)
admin.site.register(posts.Post)