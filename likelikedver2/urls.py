from django.urls import path
from . import views

urlpatterns = [
    path('authors/<int:author_id>/inbox/', views.send_like, name='send_like'),
    path('authors/<int:author_id>/posts/<int:post_id>/likes/', views.get_post_likes, name='get_post_likes'),
    path('authors/<int:author_id>/posts/<int:post_id>/comments/<int:comment_id>/likes/', views.get_comment_likes, name='get_comment_likes'),
    path('authors/<int:author_id>/liked/', views.get_liked_items, name='get_liked_items'),
]
