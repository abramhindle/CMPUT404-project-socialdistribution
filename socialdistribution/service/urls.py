from django.urls import path
from service.views.author import SingleAuthor, MultipleAuthors
from service.views.follow import FollowersAPI, FollowerAPI
from service.views.post import PostCreation, PostWithId
from service.views.comment import CommentView

urlpatterns = [
    #for every different model, create a new model file and view file in the /model and /view directories then link it up here
    path('', MultipleAuthors.as_view()), 
    path('<uuid:id>/', SingleAuthor.as_view()),
    path('<uuid:author_id>/posts/', PostCreation.as_view(), name='post_creation'),
    path('<uuid:author_id>/posts/<uuid:post_id>', PostWithId.as_view(), name='post_with_id'),
    path('<uuid:author_id>/posts/<uuid:post_id>/comments', CommentView.as_view(), name='comment_view'),
    path('<str:pk>/followers/', FollowersAPI.as_view(),name = "getfollowers"),
    path('<str:pk>/followers/<str:foreignPk>',FollowerAPI.as_view(),name="getfollower"),
]