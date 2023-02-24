from django.contrib import admin
from .models.author import Author,Followers

# Register your models here.

admin.site.register(Author)
admin.site.register(Followers)
