from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'likes_api'
urlpatterns = [
    path('inbox/', views.inbox_like.as_view(), name='inbox_like'),
    path('post/<str:post_id>/likes', views.post_likes.as_view(), name='post_likes'),
    path('post/<str:post_id>/comments/<str:comment_id>/likes', views.comment_likes.as_view(), name='comment_likes'),
    path('liked', views.author_liked.as_view(), name='liked'),
]

urlpatterns = format_suffix_patterns(urlpatterns)