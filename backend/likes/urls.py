from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.LikesViewSet, basename='likes')
router.register(r'', views.LikesCommentViewSet, basename='likes')
urlpatterns = router.urls
