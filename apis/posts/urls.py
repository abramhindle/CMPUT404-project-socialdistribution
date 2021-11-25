from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'post_api'
urlpatterns = [
    path('', views.posts.as_view(), name='posts'),
    path('<str:post_id>/', views.post.as_view(), name='post'),
    path('<str:post_id>/comments/', views.comments.as_view(), name='comments'),
]

urlpatterns = format_suffix_patterns(urlpatterns)