from django.contrib import admin
from .models import *


# Register your models here.
class AuthorProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(AuthorProfile, AuthorProfileAdmin)
admin.site.register(Category)
admin.site.register(AllowToView)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(ServerUser)
