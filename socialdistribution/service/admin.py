from django.contrib import admin
from .models.author import Author
from .models.comment import Comment

# Register your models here.

admin.site.register(Author)
admin.site.register(Comment)