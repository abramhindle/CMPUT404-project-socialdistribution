from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('site/accounts/signup/', views.SignUpView.as_view(), name='signup'),
    path('', views.IndexView, name='index'),
    path('index', views.IndexView, name='index'),
    path('site/authors', views.authors, name='authors'),
    path('site/authors/followers', views.followers, name='followers'),
    path('site/authors/<path:author_id>/followers', views.followers_with_target, name='followers_with_target'),
    path('site/authors/<path:author_id>', views.author, name='author'),
    # path('site/authors', views.authors.as_view(), name='authors'),
    # path("site/authors/<str:author_id>/followers", views.FollowerDetails.as_view(), name="author-followers"),
    # path("site/authors/<str:author_id>/followers/<str:foreign_author_id>", views.FollowerDetails.as_view(), name="follower-info"),
]