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
	list_display = ('id', 'get_user')

	def get_user(self, author):
		return author.user.username

	get_user.short_description = 'User'

class FollowAdmin(ModelAdmin):
	list_display = ('id', 'get_object', 'get_actor')

	def get_object(self, follow):
		return follow.followee.displayName

	def get_actor(self, follow):
		return follow.follower.displayName

	get_object.short_description = 'Object'
	get_actor.short_description = 'Actor'


class PostAdmin(ModelAdmin):
	list_display=('id', 'get_user', 'title')

	def get_user(self, post):
		return post.author.displayName

	get_user.short_description = 'User'

class CommentAdmin(ModelAdmin):
	list_display=('id', 'get_user', 'get_post_id', 'get_post_title')

	def get_user(self, comment):
		return comment.author.user.username

	def get_post_title(self, comment):
		return comment.post.title

	def get_post_id(self, comment):
		return comment.post.id

	get_user.short_description = 'User'
	get_post_id.short_description = 'Post'
	get_post_title.short_description = 'Title'

class InboxAdmin(ModelAdmin):
	list_display = ('id', 'get_author')
	
	def get_author(self, inbox):
		return inbox.author.displayName
		
	get_author.short_description = 'Author'

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register your models here.
admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Inbox)
admin.site.register(Node)
