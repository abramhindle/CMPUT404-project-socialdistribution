from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

# Routers provide an easy way of automatically determining the URL conf.
from service import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'authors', views.AuthorViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^friendrequest/', views.send_friend_request, name='friend-request')
]
