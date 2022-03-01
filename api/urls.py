from django.urls import include, path
from rest_framework import routers
from api.views import AuthorViewSet

router = routers.DefaultRouter()
router.register(r'authors', AuthorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
