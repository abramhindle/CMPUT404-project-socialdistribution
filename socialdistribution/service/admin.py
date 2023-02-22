from django.contrib import admin
from service.models import author, post
from .models.comment import Comment

# Register your models here.

admin.site.register(Author)
#admin.site.register(post.Post) #we don't need this here, but leaving as comment just in case
#admin.site.register(post.Category)
admin.site.register(Comment)