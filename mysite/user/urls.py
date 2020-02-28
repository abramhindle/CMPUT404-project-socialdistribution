from django.contrib import admin
from rest_framework import routers
from django.urls import path, include
from .views import AuthorViewSet

router = routers.DefaultRouter()
router.register("author", AuthorViewSet, basename="author")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("signup/", include("rest_auth.registration.urls")),
    path("", include("rest_auth.urls")),
    path("", include(router.urls)),
]
