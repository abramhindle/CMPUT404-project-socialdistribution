from django.contrib import admin
from author.models import Author, FriendRequest

admin.site.register(Author)
admin.site.register(FriendRequest)