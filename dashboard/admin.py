from django.contrib import admin

# Register your models here.
from dashboard.models import Author, Node

admin.site.register(Node)
admin.site.register(Author)
