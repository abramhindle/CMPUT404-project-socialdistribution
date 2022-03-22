from django.urls import include, path
from pyrsistent import inc
from rest_framework import routers
from api.views import AuthorViewSet, PostViewSet, LikesViewSet
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r'authors', AuthorViewSet)

author_router = routers.NestedDefaultRouter(router, r'authors', lookup='author')
author_router.register(r'posts', PostViewSet, basename='post')

like_router = routers.NestedDefaultRouter(author_router, r'posts', lookup='post')
like_router.register(r'likes', LikesViewSet, basename='likes')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(author_router.urls)),
    path('', include(like_router.urls))
]
