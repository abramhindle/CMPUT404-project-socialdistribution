from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Author)
admin.site.register(Follower)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Request)
admin.site.register(Inbox)
admin.site.register(Likes)
admin.site.register(Liked)
