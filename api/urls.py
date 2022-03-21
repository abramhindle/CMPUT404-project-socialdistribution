from django.urls import include, path
from rest_framework import routers
from api.views import AuthorViewSet, PostViewSet
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r'authors', AuthorViewSet)

author_router = routers.NestedDefaultRouter(router, r'authors', lookup='author')
author_router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(author_router.urls)),
]
