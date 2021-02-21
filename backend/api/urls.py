from django.urls import path, re_path, include
from django.conf.urls import url

from .views import index, simplePostView, author
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('', index.index, name="index"),
    path(r'author/<str:author_id>/posts/', simplePostView.createNewPost, name="post-post-view"),
    path(r'author/<str:author_id>/posts/<str:post_id>', simplePostView.handleExistPost, name="get-post-view"),
    path('api-auth/', include('rest_framework.urls')),    
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
]

