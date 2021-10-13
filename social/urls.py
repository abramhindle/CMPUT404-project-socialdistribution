from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'author', views.AuthorViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('author/<int:id>/followers', views.FollowerViewSet),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]