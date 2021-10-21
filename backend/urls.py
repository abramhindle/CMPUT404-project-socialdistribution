from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),

    # The endpoint for viewing the authors list
    path("authors/", views.authors_list_api, name="author-list"),
    # The endpoint for viewing and updating a single author
    path("author/<str:author_id>/", views.AuthorDetail.as_view(), name="author-detail"),

    # The endpoints for CRUD operations on followers
    path("author/<str:author_id>/followers", views.FollowerDetail.as_view(), name="author-followers"),
    path("author/<str:author_id>/followers/<str:foreign_author_id>", views.FollowerDetail.as_view(), name="follower-detail"),

    # The endpoints for CRUD operations on posts
    path("author/<str:author_id>/posts", views.PostDetail.as_view(), name="author-posts"),
    path("author/<str:author_id>/posts/<str:post_id>", views.PostDetail.as_view(), name="post-detail"),

    # The endpoint for viewing and updating comments
    path("author/<str:author_id>/posts/<str:post_id>/comments", views.comment_view_api, name="comment-detail"),
]