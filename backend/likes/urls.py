from rest_framework.routers import DefaultRouter
from . import views
from rest_framework.routers import DefaultRouter, DynamicRoute, Route

router = DefaultRouter()
# routes = [
#    # List routes
#         Route(
#             url=r'^{prefix}{trailing_slash}$',
#             mapping={
#                 'get': 'list',
#                 'post': 'create',
#                 'delete': 'destroy',
#             },
#             name='{basename}-list',
#             detail=False,
#             initkwargs={'suffix': 'List'}
#         ),
#         # Dynamically generated list routes. Generated using @action(detail=False) decorator on methods of the viewset.
#         DynamicRoute(
#             url=r'^{prefix}/{url_path}{trailing_slash}$',
#             name='{basename}-{url_name}',
#             detail=False,
#             initkwargs={}
#         ),
#         # Detail routes
#         Route(
#             url=r'^{prefix}/{lookup}{trailing_slash}$',
#             mapping={
#                 'get': 'retrieve',
#                 'put': 'update',
#                 'patch': 'partial_update',
#                 'delete': 'destroy'
#             },
#             name='{basename}-detail',
#             detail=True,
#             initkwargs={'suffix': 'Instance'}
#         ),
#         # Dynamically generated detail routes. Generated using @action(detail=True) decorator on methods of the viewset.
#         DynamicRoute(
#             url=r'^{prefix}/{lookup}/{url_path}{trailing_slash}$',
#             name='{basename}-{url_name}',
#             detail=True,
#             initkwargs={}
#         ),
# ]
router.register(r'', views.LikesViewSet, basename='likes')
router.register(r'', views.LikesCommentViewSet, basename='likes')
router.register(r'', views.LikesRetrievedViewSet, basename='likes')
# router.register(r'/decrement/', views.LikesDeleteViewSet, basename='likes')
urlpatterns = router.urls
