from django.urls import path
from .views import LikedView, LikesView

urlpatterns = [
    path('authors/<str:author_id>/liked/', LikedView.as_view()),
    path('authors/<str:author_id>/posts/<str:post_id>/likes/', LikesView.as_view()),
    path('authors/<str:author_id>/posts/<str:post_id>/comments/<str:comment_id>/likes/', LikesView.as_view())
]
