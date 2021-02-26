from rest_framework import routers
from .api import AuthorViewSet, PostViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register('author', AuthorViewSet, 'authors')



urlpatterns = [
    path('author/<str:id>/', AuthorViewSet.as_view({'post': 'update', 'get': 'retrieve'}), name='author_update'),
    # path('author', include(router.urls))
    path('author/<str:author_id>/posts/', PostViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('author/<str:author_id>/posts/<str:id>/', PostViewSet.as_view({'get': 'retrieve', 'post': 'update', 'delete': 'destroy', 'put': 'create'}))
]