from rest_framework import routers
from .api import AuthorViewSet, RegisterAPI, LoginAPI, UserAPI
from knox import views as knox_views
from django.urls import path, include

router = routers.DefaultRouter()
router.register('author', AuthorViewSet, 'authors')

urlpatterns = [
    path('author/<str:id>/', AuthorViewSet.as_view({'post': 'update', 'get': 'retrieve'}), name='author_update'),
    path('api/auth', include('knox.urls')),
    path('api/auth/register', RegisterAPI.as_view()),
    path('api/auth/login', LoginAPI.as_view()),
    path('api/auth/user', UserAPI.as_view())
    # path('author', include(router.urls))
]