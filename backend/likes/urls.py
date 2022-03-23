from rest_framework.routers import DefaultRouter
from . import views
from rest_framework.routers import DefaultRouter, DynamicRoute, Route

router = DefaultRouter()

router.register(r'', views.LikesViewSet, basename='likes')
router.register(r'', views.LikesCommentViewSet, basename='likes')
# router.register(r'', views.LikesRetrievedViewSet, basename='liked')
urlpatterns = router.urls
