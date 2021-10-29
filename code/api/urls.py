from django.urls import path

from .views import *

app_name = 'api'
urlpatterns = [
    path('', index, name='index'),
    path('authors/', AuthorsView.as_view(), name='authors'),
    path('author/<author_id>', AuthorView.as_view(), name='author'),
    path('author/<author_id>/followers', FollowersView.as_view(), name='followers'),
    path('author/<author_id>/liked', LikedView.as_view(), name='liked'),
    path('author/<author_id>/posts', PostsView.as_view(), name='posts'),
    path('author/<author_id>/posts/<post_id>', PostView.as_view(), name='post'),
    path('author/<author_id>/posts/<post_id>/likes', PostLikesView.as_view(), name='post_likes'),
    path('author/<author_id>/posts/<post_id>/comments', PostCommentsView.as_view(), name='post_comments'),
    path('author/<author_id>/posts/<post_id>/comments/', PostCommentsView.as_view(), name='post_comments'),
    path('author/<author_id>/posts/<post_id>/comments/<comment_id>/likes', CommentLikesView.as_view(), name='comment_likes'),
    path('author/<author_id>/inbox', InboxView.as_view(), name='inbox'),
    path('author/<author_id>/inbox/', InboxView.as_view(), name='inbox'),
]