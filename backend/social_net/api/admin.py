from django.contrib import admin
from .models import AuthorModel, PostsModel, ImageModel

# Register your models here.
admin.site.register(AuthorModel)
admin.site.register(PostsModel)
admin.site.register(ImageModel)
