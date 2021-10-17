from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('authors/', AuthorsView.as_view(), name='authors'),
    path('authors/<author_id>/', AuthorView.as_view(), name='author'),
    path('authors/<author_id>/followers/', FollowersView.as_view(), name='followers'),
    path('authors/<author_id>/liked/', LikedView.as_view(), name='liked'),
    path('authors/<author_id>/posts/<post_id>/', PostView.as_view(), name='post'),
    path('authors/<author_id>/posts/<post_id>/likes/', PostLikesView.as_view(), name='post_likes'),
    path('authors/<author_id>/posts/<post_id>/comments/', PostCommentsView.as_view(), name='post_comments'),
    path('authors/<author_id>/posts/<post_id>/comments/<comment_id>/likes/', CommentLikesView.as_view(), name='comment_likes'),
    path('authors/<author_id>/inbox/', InboxView.as_view(), name='inbox'),
]