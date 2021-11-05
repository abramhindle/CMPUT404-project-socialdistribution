from django.contrib import admin

from .models.postModel import Post
from .models.authorModel import Author
from .models.accountRegistrationModel import accountRequest
from .models.commentModel import Comment

from .views.adminView import pendingRequestView


admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Comment)


admin.site.register(accountRequest, pendingRequestView)
