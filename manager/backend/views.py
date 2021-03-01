from django.shortcuts import render
from .api import RegisterAPI, CreateAuthorAPI

# Create your views here.
def registerView(request):
    RegisterAPI.as_view({'post': 'update', 'get': 'retrieve'})
    CreateAuthorAPI.as_view({'post': 'update', 'get': 'retrieve'})