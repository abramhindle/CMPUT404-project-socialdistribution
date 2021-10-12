from django.contrib import admin
from .models import Follow, Author, Inbox

# Register your models here.
admin.site.register(Follow)
admin.site.register(Author)
admin.site.register(Inbox)