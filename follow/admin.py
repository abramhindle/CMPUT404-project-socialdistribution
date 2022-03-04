from django.contrib import admin
# Register your models here.
from .models import Follow, Request


class FollowAdmin(admin.ModelAdmin):
    model = Follow
    raw_id_feild = ("follwer", "followee")


class RequestAdmin(admin.ModelAdmin):
    model = Request
    raw_id_feild = ("from_user", "to_user")


admin.site.register(Follow, FollowAdmin)
admin.site.register(Request, RequestAdmin)
