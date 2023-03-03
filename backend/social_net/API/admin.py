from django.contrib import admin
from .models import AuthorModel, PostsModel

# Register your models here.
admin.site.register(AuthorModel)
admin.site.register(PostsModel)