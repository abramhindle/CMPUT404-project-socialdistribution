from django.conf.urls import url
from django.urls import path, include
from backend.views import *
from network.views import *

urlpatterns = [
    path('', apiOverview, name="apiOverview"),
    path('authors/', AuthorList, name ='authorList'),
    path('author/<str:author_uuid>/', AuthorDetail, name="authorDetail"),
    path('author/<str:author_uuid>/followers/', FollowerList, name="followerList"),
    path('author/<str:author_uuid>/followers/<str:follower_uuid>', FollowerDetail, name="followerDetail"),
]
