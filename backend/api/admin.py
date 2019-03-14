from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(AuthorProfile)
admin.site.register(Category)
admin.site.register(AllowToView)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(ServerNode)