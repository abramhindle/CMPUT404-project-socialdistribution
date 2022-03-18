from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.NodeViewSet, basename='nodes')
urlpatterns = router.urls
