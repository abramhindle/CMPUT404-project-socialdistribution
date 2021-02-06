from django.contrib import admin
from .models.post import Post
from .models.author import Author
from .models.comment import Comment
from .models.like import Like
from .models.follower import Follower
from .models.friend import Friend
from .models.inbox import Inbox

# Register your models here.
admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Follower)
admin.site.register(Friend)
admin.site.register(Inbox)
