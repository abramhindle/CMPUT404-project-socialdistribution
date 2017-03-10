from django.contrib import admin
from . models import Post
from .models import Comment

# Add Post to Admin Panel
admin.site.register(Post)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created')
    list_filter = ['created']
    search_fields = ('author', 'body')

# Add Comment ot Admin Panel
admin.site.register(Comment, CommentAdmin)
