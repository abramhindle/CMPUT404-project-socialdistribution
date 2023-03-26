from django.contrib import admin
from .models import AuthorModel, PostsModel, CommentsModel, LikeModel

# Register your models here.
admin.site.register(AuthorModel)
admin.site.register(PostsModel)
admin.site.register(CommentsModel)
admin.site.register(LikeModel)