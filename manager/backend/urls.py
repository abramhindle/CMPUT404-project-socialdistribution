from rest_framework import routers
from .api import AuthorViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register('author', AuthorViewSet, 'authors')



urlpatterns = [
    path('author/<str:id>/', AuthorViewSet.as_view({'post': 'update', 'get': 'retrieve'}), name='author_update'),
    path('', include(router.urls))
]