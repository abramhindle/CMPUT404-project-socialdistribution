from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path("authors/", views.authors_list_api),
    path("author/<str:id>/", views.author_view_api),
    path("author/<str:id>/followers", views.follower_api),
    path("author/<str:id>/followers/<str:foreign_id>", views.follower_api),
    path("author/<str:id>/posts", views.post_view_api),
    path("author/<str:id>/posts/<str:post_id>", views.post_view_api),
]