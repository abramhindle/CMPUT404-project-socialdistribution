from django.urls import re_path, path
from django.shortcuts import render
from service.views.author import SingleAuthor, MultipleAuthors
from service.views.follower import FollowersAPI, FollowerAPI
from service.views.follow_request import AuthorFollowRequests
from service.views.post import PostCreation, PostWithId
from service.views.inbox import InboxView
#from .views.follower_views import FollowerAPIView, FollowersAPIView
from service.views.comment import CommentView
from service.views.liked import LikedView, LikesView
from django.views.generic import TemplateView

#this shit is hell, but django freaks out trying to parse nested urls otherwise
AUTHOR_ID_REGEX = r"http://[A-Za-z0-9]+/authors/[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}"
POST_ID = r"http://[A-Za-z0-9]+/authors/[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}/posts/[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}"
COMMENT_ID_REGEX = r"http://[A-Za-z0-9]+/authors/[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}/posts/[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}/comments/[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}"

urlpatterns = [
    path('docs/', TemplateView.as_view(template_name='templates/docs/index.html'), name='docs'),
    #for every different model, create a new model file and view file in the /model and /view directories then link it up here
    re_path(rf'(?P<author_id>{AUTHOR_ID_REGEX})/posts/(?P<post_id>{POST_ID})/comments/(?P<comment_id>{COMMENT_ID_REGEX})/', LikesView.as_view(), name='post_likes'),
    re_path(rf'(?P<author_id>{AUTHOR_ID_REGEX})/follow-request/', AuthorFollowRequests.as_view(),name="author_request"),
    re_path(rf'(?P<author_id>{AUTHOR_ID_REGEX})/followers/(?P<foreign_author_id>{AUTHOR_ID_REGEX})', FollowerAPI.as_view(),name="getfollower"),
    re_path(rf'(?P<author_id>{AUTHOR_ID_REGEX})/followers/', FollowersAPI.as_view(),name = "getfollowers"),
    re_path(rf'(?P<author_id>{AUTHOR_ID_REGEX})/posts/(?P<post_id>{POST_ID})/likes/', LikesView.as_view(), name='post_likes'),
    re_path(rf'^(?P<author_id>{AUTHOR_ID_REGEX})/posts/(?P<post_id>{POST_ID})/comments/$', CommentView.as_view(), name='comment_view'),
    re_path(rf'^(?P<author_id>{AUTHOR_ID_REGEX})/posts/(?P<post_id>{POST_ID})/$', PostWithId.as_view(), name='post_with_id'),
    re_path(rf'^(?P<author_id>{AUTHOR_ID_REGEX})/liked/', LikedView.as_view(), name='author_likes'),
    re_path(rf'^(?P<author_id>{AUTHOR_ID_REGEX})/posts/$', PostCreation.as_view(), name='post_creation'),
    re_path(rf'^(?P<author_id>{AUTHOR_ID_REGEX})/inbox/$', InboxView.as_view(), name='inbox_view'),
    re_path(rf'^(?P<author_id>{AUTHOR_ID_REGEX})/$', SingleAuthor.as_view()),
    re_path(r'^$', MultipleAuthors.as_view()), 
]
