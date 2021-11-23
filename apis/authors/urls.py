from django.urls import path

from . import views

app_name = 'author'
urlpatterns = [
    path('author/<str:author_id>', views.author.as_view(), name='author'),
    path('authors', views.authors.as_view(), name='authors'),
    path("author/<str:author_id>/followers", views.FollowerDetails.as_view(), name="author-followers"),
    path("author/<str:author_id>/followers/<str:foreign_author_id>", views.FollowerDetails.as_view(), name="follower-info"),

]