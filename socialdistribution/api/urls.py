from django.urls import path

from . import views

urlpatterns = [
    path(
        "posts",
        views.posts,
        name="api_get_all_public_posts"),
    path(
        "posts/<uuid:post_id>",
        views.single_post,
        name="api_get_single_post"),
    path(
        "posts/<uuid:post_id>/comments",
        views.post_comments,
        name="api_post_comments"),
    path(
        "author/posts",
        views.author_posts,
        name="api_get_author_posts"),
    path(
        "author/<uuid:author_id>",
        views.author_profile,
        name="api_get_author_profile"),
    path(
        "author/<uuid:author_id>/posts",
        views.specific_author_posts,
        name="api_get_specific_author_posts"),
    path(
        "author/<uuid:author_uuid>/friends",
        views.author_friends,
        name="api_get_author_friends"),
    path(
        "author/<uuid:author_uuid>/friends/<path:author_friend_url>",
        views.author_friends_with_author,
        name="api_get_author_friends_with_author"),
    path(
        "friendrequest",
        views.friend_request,
        name="api_friend_request"),
    path(
        "whoami",
        views.who_am_i,
        name="api_who_am_i"),
    path(
        "cansee/<uuid:author_id>/<uuid:post_id>",
        views.can_see,
        name="api_can_see"),
]
