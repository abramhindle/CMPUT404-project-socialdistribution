from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.CommentViewSet, basename='comment')
urlpatterns = router.urls
