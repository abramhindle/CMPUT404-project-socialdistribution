from django.contrib import admin
from .models import AuthorModel, PostsModel, ImageModel, CommentsModel, LikeModel, FollowModel, InboxModel, NodeModel

# Register your models here.
admin.site.register(AuthorModel)
admin.site.register(PostsModel)
admin.site.register(ImageModel)
admin.site.register(CommentsModel)
admin.site.register(LikeModel)
admin.site.register(FollowModel)
admin.site.register(InboxModel)
admin.site.register(NodeModel)
