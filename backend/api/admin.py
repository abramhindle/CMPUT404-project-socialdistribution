from django.contrib import admin
from .models.post import Post
from .models.author import Author
from .models.signupRequest import Signup_Request
from .models.comment import Comment
from .models.like import Like
from .models.follower import Follower
from .models.friend import Friend
from .models.inbox import Inbox
from django.conf import settings

# Register your models here.
admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Follower)
admin.site.register(Friend)
admin.site.register(Inbox)


# move request info to Author table with generated url
# args
#       ModelAdmin
#       request
#       queryset (selected requests)
# return
#       None
def accept_signup_request(ModelAdmin, request, queryset):
    for req in queryset:
        a = Author(username=req.username, password=req.password, host = settings.HOST_URL, git_url=req.git_url)
        a.url = f'{settings.HOST_URL}author/{a.id}'
        a.save()
    queryset.delete()

accept_signup_request.short_description = "allow them to be on server"

# admin list view for signup requests
class signup_request_admin(admin.ModelAdmin):
    list_display = ['username', 'git_url']
    ordering = ['username']
    actions = [accept_signup_request]

admin.site.register(Signup_Request, signup_request_admin)
