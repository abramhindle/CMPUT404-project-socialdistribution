from rest_framework import routers
from .api import AuthorViewSet, CommentViewSet, LikeAPI, NameAPI, RegisterAPI, PostViewSet, LoginAPI, LikedAPI, InboxAPI
from django.urls import path, include
from rest_framework.authtoken import views

router = routers.DefaultRouter()
router.register('author', AuthorViewSet, 'authors')

urlpatterns = [

	# Author
	path('author/<str:id>/', AuthorViewSet.as_view({'post': 'update', 'get': 'retrieve'}), name='author_update'),
	path('api/auth/register', RegisterAPI.as_view()),
	path('api/auth/login', LoginAPI.as_view({'post':'update'})),

	# Posts
	path('author/<str:author_id>/posts/', PostViewSet.as_view({'get': 'list', 'post': 'create'})),
	path('author/<str:author_id>/posts/<str:id>/', PostViewSet.as_view({'get': 'retrieve', 'post': 'update', 'delete': 'destroy', 'put': 'create'})),

	# Comments
	path('author/<str:author_id>/posts/<str:post_id>/comments', CommentViewSet.as_view({'get':'list', 'post':'create'})),

	# Likes
	path('author/<str:author_id>/post/<str:post_id>/likes', LikeAPI.as_view({'get':'list'})),
	path('author/<str:author_id>/post/<str:post_id>/comments/<str:comment_id>/likes', LikeAPI.as_view({'get':'list'})),
	path('author/<str:author_id>/liked', LikedAPI.as_view({'get':'list'})),

	# Querying
	path('api/query/displayName', NameAPI.as_view({'post':'list'})),

	# Inbox
	path('author/<str:author_id>/inbox', InboxAPI.as_view({'get':'list', 'post':'create'})),

]