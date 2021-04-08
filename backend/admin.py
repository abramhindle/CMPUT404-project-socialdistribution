from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Author, Comment, Like, Post, Follow, Inbox, Node

class NodeInline(admin.StackedInline):
	model = Node
	can_delete = True
	verbose_name_plural = 'node'

class UserAdmin(UserAdmin):
	inlines = (NodeInline,)
	list_filter = (
		('node', admin.RelatedOnlyFieldListFilter),
		'is_active',
		'is_staff',
		'is_superuser',
	)
	list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'node_check')

	def node_check(self, user):
		if not user.node.remote_username == "":
			return user.node.host

	node_check.short_description = 'Node'

class AuthorAdmin(ModelAdmin):
	list_display = ('author', 'user')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register your models here.
admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Follow)
admin.site.register(Inbox)
admin.site.register(Node)
