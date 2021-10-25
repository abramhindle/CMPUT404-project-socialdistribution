from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'post_model'
urlpatterns = [
    path('<str:post_id>/', views.post.as_view(), name='post'),
    path('', views.posts.as_view(), name='posts'),
]

urlpatterns = format_suffix_patterns(urlpatterns)