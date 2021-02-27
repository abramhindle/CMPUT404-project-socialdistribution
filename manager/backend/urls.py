from rest_framework import routers
from .api import AuthorViewSet, RegisterAPI, LoginAPI
from django.urls import path, include
from rest_framework.authtoken import views

router = routers.DefaultRouter()
router.register('author', AuthorViewSet, 'authors')

urlpatterns = [
    path('author/<str:id>/', AuthorViewSet.as_view({'post': 'update', 'get': 'retrieve'}), name='author_update'),
    path('api/auth/register', RegisterAPI.as_view()),
    path('api/auth/login', views.obtain_auth_token),
    # path('author', include(router.urls))
]