from posts import views
from django.urls import path

app_name = 'posts'
urlpatterns = [
    path('new', views.CreatePostView.as_view(), name='new'),
]
