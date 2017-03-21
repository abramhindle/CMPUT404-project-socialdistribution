from django.conf.urls import url, include
from rest_framework import routers
from service.views import authors, friendrequest, users

# Routers provide an easy way of automatically determining the URL conf.
from service import views

router = routers.DefaultRouter()
router.register(r'users', users.UserViewSet)
router.register(r'authors', authors.AuthorViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^friendrequest/', friendrequest.friendrequest, name='friend-request'),
]
