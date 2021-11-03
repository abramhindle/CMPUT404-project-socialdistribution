from django.contrib import admin
from django.contrib.auth.hashers import make_password
from ..models.authorModel import Author

# DJANGO ADMIN PANEL
# Allows you to view pending request to action on
def pendingRequest(ModelAdmin,request, result):
    for request in result:
        admin = Author(displayName=request.displayName ,username=request.username, password=make_password(request.password), host = request.host, github=request.github)
        admin.url = (f'{request.host}author/{admin.authorID}')
        admin.save()
    result.delete()

pendingRequest.short_description = "ACCEPT USER REQUEST"

# Admin pending request
class pendingRequestView(admin.ModelAdmin):
    list_display = ['username','displayName', 'github', 'host']
    ordering = ['username']
    actions = [pendingRequest]
