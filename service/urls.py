from django.conf.urls import url, include
from rest_framework import routers

import service.authors.views
import service.friendrequest.views
import service.users.views

router = routers.DefaultRouter()
router.register(r'users', service.users.views.UserViewSet)
router.register(r'authors', service.authors.views.AuthorViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^friendrequest/', service.friendrequest.views.friendrequest, name='friend-request'),
]
