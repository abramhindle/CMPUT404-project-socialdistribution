from django.contrib import admin

from social.app.models.author import Author
from social.app.models.comment import Comment
from social.app.models.node import Node
from social.app.models.post import Post

admin.site.register(Node)
admin.site.register(Author)

admin.site.register(Post)


# Add Comment to Admin Panel

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created')
    list_filter = ['created']
    search_fields = ('author', 'body')


admin.site.register(Comment, CommentAdmin)
