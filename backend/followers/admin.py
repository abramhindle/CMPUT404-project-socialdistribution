from django.contrib import admin
from .models import Following, Follower


class FollowersAdmin(admin.ModelAdmin):

    ordering = ('id',)
    search_fields = ('get_author',)
    list_display = ('id', 'summary', 'get_author')

    def get_author(self, obj: Follower):
        return obj.object.displayName


class FollowingAdmin(admin.ModelAdmin):

    ordering = ('id',)
    search_fields = ('get_author',)
    list_display = ('id', 'get_author', 'follows')

    def get_author(self, obj: Following):
        return obj.author.displayName


admin.site.register(Follower, FollowersAdmin)
admin.site.register(Following, FollowingAdmin)
