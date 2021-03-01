from rest_framework import routers
from .api import AuthorViewSet, RegisterAPI, PostViewSet, CreateAuthorAPI, LoginAPI
from .views import registerView
from django.urls import path, include
from rest_framework.authtoken import views

router = routers.DefaultRouter()
router.register('author', AuthorViewSet, 'authors')

urlpatterns = [
    path('author/<str:id>/', AuthorViewSet.as_view({'post': 'update', 'get': 'retrieve'}), name='author_update'),
    path('api/auth/register', RegisterAPI.as_view()),
    
    #path('author/create', CreateAuthorAPI.as_view({'post': 'create'})),
    path('author/create', CreateAuthorAPI.as_view()),

    path('api/auth/login', LoginAPI.as_view({"get":"list"})),

    # path('author', include(router.urls))
    path('author/<str:author_id>/posts/', PostViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('author/<str:author_id>/posts/<str:id>/', PostViewSet.as_view({'get': 'retrieve', 'post': 'update', 'delete': 'destroy', 'put': 'create'}))
]