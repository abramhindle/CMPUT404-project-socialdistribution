from rest_framework import routers
from .api import AuthorViewSet, RegisterAPI, PostViewSet, LoginAPI
from django.urls import path, include
from rest_framework.authtoken import views

router = routers.DefaultRouter()
router.register('author', AuthorViewSet, 'authors')

urlpatterns = [
    path('author/<str:author_id>/', AuthorViewSet.as_view({'post': 'update', 'get': 'retrieve'}), name='author_update'),
    path('api/auth/register', RegisterAPI.as_view()),
    path('api/auth/login', views.obtain_auth_token),
    path('author/<str:author_id>/posts/', PostViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('author/<str:author_id>/posts/<str:id>/', PostViewSet.as_view({'get': 'retrieve', 'post': 'update', 'delete': 'destroy', 'put': 'create'}))
]