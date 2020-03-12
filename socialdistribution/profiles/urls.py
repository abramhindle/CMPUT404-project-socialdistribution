from django.urls import path
from profiles import views

urlpatterns = [
    path('', views.new_post, name='author-profile'),
    path('posts/', views.current_visible_posts, name='visible-posts'),
    path('<uuid:author_id>/posts/', views.author_posts, name='author-posts'),
    path(
        'author/<uuid:author_id>/profile', views.view_author_profile, name='view_author_profile'
    ),
    
    # path('editprofile/', views.edit_profile, name='editprofile'),
]
