from django.urls import path
from . import views


urlpatterns = [
   path('authors/<slug:author_id>/posts/<slug:post_id>/', views.PostsRetriveView, name='PostsRetriveView'),
    path('authors/<slug:author_id>/posts/', views.PostsView, name='PostsView'),
    path('authors/<slug:author_id>/inbox/', views.inbox, name='inbox'),
    path('authors/<slug:author_id>/posts/<slug:post_id>/likes/', views.post_likes, name='post_likes'),
    path('authors/<slug:author_id>/posts/<slug:post_id>/comments/<slug:comment_id>/likes/', views.comment_likes, name='comment_likes'),
    path('authors/<slug:author_id>/liked/', views.liked, name='liked'),
    path('authors/<slug:author_id>/inbox/', views.inbox, name='inbox'),
]