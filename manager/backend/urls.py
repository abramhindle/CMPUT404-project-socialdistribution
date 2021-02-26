from rest_framework import routers
from .api import AuthorViewSet

router = routers.DefaultRouter()
router.register('author', AuthorViewSet, 'authors')



urlpatterns = router.urls