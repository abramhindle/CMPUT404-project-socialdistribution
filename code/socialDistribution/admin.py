from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Category)