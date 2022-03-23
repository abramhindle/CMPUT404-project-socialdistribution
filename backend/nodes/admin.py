from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe    
from .models import Node


class NodeAdmin(admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ('name', 'host')
    list_display = ('name', 'host', 'username', 'password')


admin.site.register(Node, NodeAdmin)
