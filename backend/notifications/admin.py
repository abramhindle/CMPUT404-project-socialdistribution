from django.contrib import admin
from .models import Notification


class NotificationAdmin(admin.ModelAdmin):

    ordering = ('published',)
    search_fields = ('get_author',)
    list_display = ('id', 'get_author', 'published', 'summary')

    def get_author(self, obj: Notification):
        return obj.author.displayName


admin.site.register(Notification, NotificationAdmin)
