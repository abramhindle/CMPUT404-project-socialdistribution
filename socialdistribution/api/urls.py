from django.urls import path

from . import views

urlpatterns = [
    path("posts", views.posts, name="api_get_all_public_posts"),
    path("posts/<uuid:post_id>", views.single_post, name="api_get_single_post"),
    path("posts/<uuid:post_id>/comments", views.post_comments, name="api_get_post_comments"),
    path("author/<uuid:author_id>/posts", views.specific_author_posts, name="api_get_specific_author_posts"),
    path("author/posts", views.author_posts, name="api_get_author_posts")
]