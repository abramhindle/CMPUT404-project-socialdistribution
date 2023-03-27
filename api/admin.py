from django.contrib import admin
from .models import AuthorModel, PostsModel, ImageModel, CommentsModel, LikeModel, FollowModel

# Register your models here.
admin.site.register(AuthorModel)
admin.site.register(PostsModel)
admin.site.register(ImageModel)
admin.site.register(CommentsModel)
admin.site.register(LikeModel)
admin.site.register(FollowModel)
