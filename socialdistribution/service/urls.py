from django.urls import re_path, path
from service.views.author import SingleAuthor, MultipleAuthors
from service.views.follow import FollowersAPI, FollowerAPI
from service.views.post import PostCreation, PostWithId
from service.views.inbox import InboxView
#from .views.follower_views import FollowerAPIView, FollowersAPIView
from service.views.comment import CommentView


#this shit is hell, but django freaks out trying to parse nested urls otherwise
AUTHOR_ID_REGEX = r"http://[A-Za-z0-9]+/authors/[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}"
POST_ID = r"http://[A-Za-z0-9]+/authors/[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}/posts/[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}"
POST_ID_REGEX = rf"http://[A-Za-z0-9]+/authors/{AUTHOR_ID_REGEX}/posts/{POST_ID}"

urlpatterns = [
    #for every different model, create a new model file and view file in the /model and /view directories then link it up here
    # path('service/authors/<str:author>/followers', FollowersAPIView.as_view(), name='service-followers'),
    # path('service/authors/<str:author>/followers/<str:another_author>', FollowerAPIView.as_view(), name='service-follower'),
    re_path(rf'^(?P<author_id>{AUTHOR_ID_REGEX})/posts/(?P<post_id>{POST_ID})/comments/$', CommentView.as_view(), name='comment_view'),
    re_path(rf'^(?P<author_id>{AUTHOR_ID_REGEX})/posts/(?P<post_id>{POST_ID})/$', PostWithId.as_view(), name='post_with_id'),
    re_path(rf'^(?P<author_id>{AUTHOR_ID_REGEX})/posts/$', PostCreation.as_view(), name='post_creation'),
    re_path(rf'^(?P<author_id>{AUTHOR_ID_REGEX})/inbox/$', InboxView.as_view(), name='inbox_view'),
    re_path(rf'^(?P<author_id>{AUTHOR_ID_REGEX})/$', SingleAuthor.as_view()),
    re_path(r'^$', MultipleAuthors.as_view()), 
    path('<str:pk>/followers/', FollowersAPI.as_view(),name = "getfollowers"), #going to to need to fix the ids on this
    path('<str:pk>/followers/<str:foreignPk>',FollowerAPI.as_view(),name="getfollower"),
]
