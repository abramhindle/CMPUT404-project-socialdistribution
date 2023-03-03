from django.urls import path
from . import views


urlpatterns = [
  path('authors/<slug:uid>', views.AuthorView, name='AuthorView'),
  path('authors/<slug:uid>/followers/', views.AuthorFollowersView, name='AuthorFollowersView'),
  path('authors/<slug:uid>/followers/<slug:foreign_uid>', views.AuthorFollowersOperationsView, name='AuthorFollowersOperationsView'),
  path('authors', views.AuthorsView, name='AuthorsView'),
  path('follow/<slug:uid>/<slug:uid2>', views.FollowView, name='FollowView'),
  path('authors/<slug:author_id>/posts/<slug:post_id>/comments', views.CommentsView, name='CommentsView'),
  path('authors/<slug:author_id>/posts/<slug:post_id>/', views.PostsRetriveView, name='PostsRetriveView'),
  path('authors/<slug:author_id>/posts/', views.PostsView, name='PostsView'),
  path('authors/<slug:author_id>/inbox/', views.InboxView, name='InboxView'),
  path('authors/<slug:author_id>/posts/<slug:post_id>/likes/', views.PostLikeView, name='PostLikeView'),
  path('authors/<slug:author_id>/posts/<slug:post_id>/comments/<slug:comment_id>/likes/', views.CommentLikeView, name='CommentLikeView'),
]