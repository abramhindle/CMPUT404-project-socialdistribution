from django.urls import path
from .views import Post

urlpatterns = [
    path('service/author/', Post, name='Post'),
]