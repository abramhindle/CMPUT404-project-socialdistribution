from . import views
from rest_framework.routers import DefaultRouter, DynamicRoute, Route


class CustomRouter(DefaultRouter):
    """
    a custom URL router for the Product API that correctly routes
    DELETE requests with multiple query parameters.

    Source: https://stackoverflow.com/a/58933387/16846929
    Author: Tobias Ernst - https://stackoverflow.com/users/3298964/tobias-ernst
    """
    routes = [
        # List routes
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create',
                'delete': 'destroy',
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        # Dynamically generated list routes. Generated using @action(detail=False) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=False,
            initkwargs={}
        ),
        # Detail routes
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        ),
        # Dynamically generated detail routes. Generated using @action(detail=True) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{lookup}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        ),
    ]


router = CustomRouter()
router.register(r'', views.InboxItemList, basename='posts')
urlpatterns = router.urls
