from django.contrib import admin
from .models import InboxItem


class InboxItemAdmin(admin.ModelAdmin):

    ordering = ('published',)
    search_fields = ('get_author',)
    list_display = ('id', 'get_author', 'src', "published")

    def get_author(self, obj):
        return obj.owner.displayName


admin.site.register(InboxItem, InboxItemAdmin)
