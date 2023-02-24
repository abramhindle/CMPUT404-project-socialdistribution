from django.urls import path
from service.views.author import SingleAuthor, MultipleAuthors
from service.views.post import PostCreation, PostWithId
from service.views.inbox import InboxView
#from .views.follower_views import FollowerAPIView, FollowersAPIView
from service.views.comment import CommentView

urlpatterns = [
    #for every different model, create a new model file and view file in the /model and /view directories then link it up here
    # path('service/authors/<str:author>/followers', FollowersAPIView.as_view(), name='service-followers'),
    # path('service/authors/<str:author>/followers/<str:another_author>', FollowerAPIView.as_view(), name='service-follower'),
    path('', MultipleAuthors.as_view()), 
    path('<path:author_id>/', SingleAuthor.as_view()),
    path('<path:author_id>/posts/', PostCreation.as_view(), name='post_creation'),
    path('<path:author_id>/posts/<path:post_id>', PostWithId.as_view(), name='post_with_id'),
    path('<path:author_id>/posts/<path:post_id>/comments', CommentView.as_view(), name='comment_view'),
    path('<uuid:author_id>/inbox', InboxView.as_view(), name='inbox_view')
]