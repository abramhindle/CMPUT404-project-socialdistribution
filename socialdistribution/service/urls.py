from django.urls import path
from service.views.author import SingleAuthor, MultipleAuthors
from service.views.follow import FollowersAPI, FollowerAPI
from service.views.post import PostCreation, PostWithId
from service.views.comment import CommentView
from service.views.follow import FollowerAPI, Followers
from service.views.likes import LikesView
from service.views.liked import LikedView

urlpatterns = [
    #for every different model, create a new model file and view file in the /model and /view directories then link it up here
    path('authors/<uuid:author>/posts/<uuid:post>/likes/', LikesView.as_view(), name='post-likes'),
    path('authors/<uuid:author>/posts/<uuid:post>/comments/<uuid:comment>/likes/', LikesView.as_view(), name='comment-likes'),
    path('authors/<uuid:author>/liked/', LikedView.as_view(), name='liked'),

    path('authors/', MultipleAuthors.as_view()), 
    path('authors/<uuid:id>/', SingleAuthor.as_view()),
    path('authors/<uuid:author_id>/posts/', PostCreation.as_view(), name='post_creation'),
    path('authors/<uuid:author_id>/posts/<uuid:post_id>', PostWithId.as_view(), name='post_with_id'),
    path('<uuid:author_id>/posts/<uuid:post_id>/comments', CommentView.as_view(), name='comment_view'),
    path('<str:pk>/followers/', FollowersAPI.as_view(),name = "getfollowers"),
    path('<str:pk>/followers/<str:foreignPk>',FollowerAPI.as_view(),name="getfollower"),
]