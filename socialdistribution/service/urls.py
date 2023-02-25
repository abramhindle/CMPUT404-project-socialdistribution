from django.urls import path
from service.views.author import SingleAuthor, MultipleAuthors
from service.views.post import PostCreation, PostWithId
from .views.follower_views import FollowerAPIView, FollowersAPIView
from .views.likes import CommentLikesView, PostLikesView
from .views.liked import LikedView

urlpatterns = [
    #for every different model, create a new model file and view file in the /model and /view directories then link it up here
    path('authors/<str:author>/followers', FollowersAPIView.as_view(), name='service-followers'),
    path('authors/<str:author>/followers/<str:another_author>', FollowerAPIView.as_view(), name='service-follower'),

    path('authors/<uuid:author>/posts/<uuid:post>/likes/', PostLikesView.as_view(), name='post-likes'),
    path('authors/<uuid:author>/posts/<uuid:post>/comments/<uuid:comment>/likes/', CommentLikesView.as_view(), name='comment-likes'),
    path('authors/<uuid:author>/liked/', LikedView.as_view(), name='liked'),

    path('authors/', MultipleAuthors.as_view()), 
    path('authors/<uuid:id>/', SingleAuthor.as_view()),
    path('authors/<uuid:author_id>/posts/', PostCreation.as_view(), name='post_creation'),
    path('authors/<uuid:author_id>/posts/<uuid:post_id>', PostWithId.as_view(), name='post_with_id')
]