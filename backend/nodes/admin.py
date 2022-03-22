from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe    
from .models import Node
# Register your models here.

class NodeAdmin(admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ('name', 'host')
    list_display = ('name', 'host', 'username', 'password', 'user_link')
    readonly_fields = ('user_link',)

    def user_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:auth_user_change", args=(obj.remote_credentials.pk,)),
            obj.remote_credentials.username
        ))
    user_link.short_description = 'remote credentials'

admin.site.register(Node, NodeAdmin)