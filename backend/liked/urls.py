from rest_framework.routers import DefaultRouter
from . import views
from rest_framework.routers import DefaultRouter, DynamicRoute, Route

router = DefaultRouter()


router.register(r'', views.LikedRetrievedViewSet, basename='liked')
urlpatterns = router.urls
