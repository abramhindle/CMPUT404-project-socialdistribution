from django.contrib import admin
from .models import Author, Avatar


class AuthorAdmin(admin.ModelAdmin):
    ordering = ('displayName',)
    search_fields = ('displayName',)
    list_display = ('displayName', 'verified')


class AvatarAdmin(admin.ModelAdmin):
    ordering = ('author',)
    search_fields = ('author',)
    list_display = ('id', 'author')

    def get_author(self, obj: Avatar):
        return obj.author.displayName


admin.site.register(Author, AuthorAdmin)
admin.site.register(Avatar, AvatarAdmin)
