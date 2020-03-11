from django.contrib import admin
from profiles.models import Author, AuthorFriend

# Register Author and AuthorFriend model in admin.
admin.site.register(Author)
admin.site.register(AuthorFriend)
