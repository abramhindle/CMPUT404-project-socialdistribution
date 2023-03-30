from django.urls import path
from . import views

urlpatterns = [
    path('authors/', views.AuthorsView.as_view(), name='Index'),
    path('authors/<str:author_id>', views.AuthorView.as_view(), name='Author'),
    path('authors/<str:author_id>/image', views.ImageView.as_view(), name='Author Image'),
    path('authors/<str:author_id>/followers', views.FollowersView.as_view(), name='Followers'),
    path('authors/<str:author_id>/followers/<str:foreign_author_id>', views.FollowView.as_view(), name='Follow'),
    path('authors/<str:author_id>/posts/', views.PostsView.as_view(), name='Posts'),
    path('authors/<str:author_id>/posts/<str:post_id>', views.PostView.as_view(), name='Post'),
    path('authors/<str:author_id>/posts/<str:post_id>/image', views.ImageView.as_view(), name='Post Image'),
    path('authors/<str:author_id>/posts/<str:post_id>/comments', views.CommentsView.as_view(), name='Comments'),
    path('authors/<str:author_id>/posts/<str:post_id>/likes', views.LikeView.as_view(), name='Likes'),
    path('authors/<str:author_id>/posts/<str:post_id>/comments/<str:comment_id>/likes', views.GetLikeCommentView.as_view(), name='Comment Likes'),
    path('authors/<str:author_id>/liked', views.LikedView.as_view(), name='Liked'),
    path('authors/<str:author_id>/inbox/', views.InboxView.as_view(), name='Inbox'),
    
    # path('authors/<str:author_id>/share/<str:encoded_post_url>/<str:encoded_destination_author_url>', views.ShareView.as_view(), name='Share'), 
    
    path('nodes/', views.NodeView.as_view(), name='Node Request'),
]