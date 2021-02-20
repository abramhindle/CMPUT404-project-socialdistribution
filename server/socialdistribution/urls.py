from django.urls import path
from .api_views import author_view
from .api_views import post_view
from .api_views import friend_view

urlpatterns = [
    # author
    path('service/author/', author_view.register),
    path('service/author/login/', author_view.login_view),
    path('service/author/logout/', author_view.logout_view),
    path('service/author/<str:authorID>/', author_view.author_detail),

    # post
    path('service/author/<str:authorID>/posts/', post_view.post_view),
    path('service/author/<str:authorID>/posts/<uuid:postID>/', post_view.post_detail_view),

    # follower
    path('service/author/<str:authorID>/followers/', friend_view.follower_list),
    path('service/author/<str:authorID>/followers/<str:foreignAuthorID>/', friend_view.follower),

    #comment
    path('service/author/<str:authorID>/posts/<uuid:postID>/comments', comment_view.comment_view),
]
