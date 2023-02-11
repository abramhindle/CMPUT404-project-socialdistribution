from django.contrib import admin

# Register your models here.
from .models import Author, Authors

admin.site.register(Authors)
admin.site.register(Author)
