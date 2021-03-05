from rest_framework import routers
#from .api import AuthorViewSet, CommentViewSet, RegisterAPI, PostViewSet, LoginAPI
from .api import AuthorViewSet, RegisterAPI, PostViewSet, LoginAPI
from django.urls import path, include
from rest_framework.authtoken import views

router = routers.DefaultRouter()
router.register('author', AuthorViewSet, 'authors')

urlpatterns = [
	#TODO path('author/<str:author_id>/inbox'),


    path('author/<str:id>/', AuthorViewSet.as_view({'post': 'update', 'get': 'retrieve'}), name='author_update'),
    path('api/auth/register', RegisterAPI.as_view()),
    path('api/auth/login', LoginAPI.as_view({'post':'update'})),
    path('author/<str:author_id>/posts/', PostViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('author/<str:author_id>/posts/<str:id>/', PostViewSet.as_view({'get': 'retrieve', 'post': 'update', 'delete': 'destroy', 'put': 'create'})),
    # path('author/<str:author_id>/posts/<str:post_id>/comments', CommentViewSet.as_view({'get':'list', 'post':'create'})),


    #TODO path('author/<str:author_id>/post/<str:post_id>/likes'),
    #TODO path('author/<str:author_id>/post/<str:post_id>/comments/<str:comment_id>/likes'),
]