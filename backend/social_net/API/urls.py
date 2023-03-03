from django.urls import path, include
# from . import views
from . import followers, authors, comments, liked, likes, posts
from API.authors import views
from API.followers import views
from API.comments import views
from API.liked import views
from API.likes import views
from API.posts import views
# from API import views

urlpatterns = [
    path('', include('API.authors.urls')),
    path('', include('API.comments.urls')),
    path('', include('API.followers.urls')),
    path('', include('API.liked.urls')),
    path('', include('API.likes.urls')),
    path('', include('API.posts.urls')),
]