from django.urls import path, re_path, include
from django.conf.urls import url

from .views import index, simplePostView, author


urlpatterns = [
    path('', index.index, name="index"),
    path(r'author/<str:author_id>/posts/', simplePostView.createNewPost, name="post-post-view"),
    path(r'author/<str:author_id>/posts/<str:post_id>', simplePostView.handleExistPost, name="get-post-view"),
    path('api-auth/', include('rest_framework.urls')),    
]

