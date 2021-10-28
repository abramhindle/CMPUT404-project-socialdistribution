from django.urls import path

from . import views

app_name = 'core'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('index', views.IndexView.as_view(), name='index'),
    path("author/<str:author_id>/followers", views.FollowerDetails.as_view(), name="authorFollowers"),
    path("author/<str:author_id>/followers/<str:foreign_author_id>", views.FollowerDetails.as_view(), name="followerInfo")
]