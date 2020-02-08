from django.contrib import admin

from .models import (AuthorId,
                     AuthorProfile)
# Register your models here.

admin.site.register(AuthorId)
admin.site.register(AuthorProfile)