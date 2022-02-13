from django.contrib import admin
from .models import Author


class AuthorAdmin(admin.ModelAdmin):
    ordering = ('displayName',)
    search_fields = ('displayName',)
    list_display = ('displayName', 'verified')


admin.site.register(Author, AuthorAdmin)
