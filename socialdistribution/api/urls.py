from django.urls import path

from . import views

urlpatterns = [
    path("posts", views.all_posts, name="api_all_posts"),
    path("posts/<uuid:post_id>", views.single_post, name="api_single_post"),
    path("posts/<uuid:post_id>/comments", views.post_comments, name="api_post_comments"),
    path("author/<uuid:author_id>/posts", views.author_posts, name="api_author_posts"),
]