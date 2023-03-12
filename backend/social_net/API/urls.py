from django.urls import path, include, re_path
# from . import views

from API import views

urlpatterns = [
  path('authors/<slug:uid>', views.AuthorView, name='AuthorView'),
  path('authors/<slug:uid>/followers', views.AuthorFollowersView, name='AuthorFollowersView'),
  path('authors/<slug:uid>/followers<slug:foreign_uid>', views.AuthorFollowersOperationsView, name='AuthorFollowersOperationsView'),
  path('authors/', views.AuthorsView, name='AuthorsView'),     # CHANGED: "authors" to "authors/"
  path('authors/<slug:author_uid>/followers/<slug:foreign_uid>', views.FollowView, name='FollowView'),
  path('authors/<slug:author_id>/posts/<slug:post_id>/comments', views.CommentsView, name='CommentsView'),
  path('authors/<slug:author_id>/posts/<slug:post_id>', views.PostsRetriveView, name='PostsRetriveView'),
  path('authors/<slug:author_id>/posts/', views.PostsView, name='PostsView'),    # CHANGED: "/posts" to "/posts/"
  path('authors/<slug:author_id>/inbox/', views.InboxView, name='InboxView'),    # CHANGED: "/inbox" to "/inbox/"
  path('authors/<slug:author_id>/posts/<slug:post_id>/likes', views.PostLikeView, name='PostLikeView'),
  path('authors/<slug:author_id>/posts/<slug:post_id>/comments/<slug:comment_id>/likes', views.CommentLikeView, name='CommentLikeView'),
  path('authors/<slug:author_id>/liked', views.LikedView, name='LikedView'),
  path('search', views.SearchView, name='SearchView')
]