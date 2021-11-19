from django.contrib import admin

from .models.accountRegistrationModel import accountRequest
from .models.authorModel import Author
from .models.friendRequestModel import FriendRequest as Friend
from .models.postModel import Post
from .models.likeModel import Like
from .models.commentModel import Comment
from .models.inboxModel import Inbox
from .models.nodeModel import Node

from .views.adminView import pendingRequestView


admin.site.register(Author)
admin.site.register(Friend)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Inbox)
admin.site.register(Like)
admin.site.register(Node)




admin.site.register(accountRequest, pendingRequestView)
