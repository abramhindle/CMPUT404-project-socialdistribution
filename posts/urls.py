from django.urls import path
from .views import AdminUserView
from .views import UserView
from .views import PostView
from .views import UserViewID
from .views import PostViewID
from .views import CommentViewList
from posts.viewsfolder.author_following_views import FriendListView, FriendRequestView
from posts.viewsfolder.author_following_views import AreFriendsView
from posts.viewsfolder.author_following_views import FollowView
from posts.viewsfolder.author_following_views import FollowReqListView
from .views import FrontEndPostViewID
from .views import FrontEndCommentView
from .views import FrontEndUserEditView
from .views import PostCreateView
from .viewsfolder.feed_views import FrontEndPublicPosts
from .viewsfolder.feed_views import FrontEndAuthorPosts
from .viewsfolder.feed_views import FrontEndFeed
from .viewsfolder.login_reg_view import RegistrationPageView
from .viewsfolder.login_reg_view import LoginPageView
from .viewsfolder.author_following_views import AuthorViewFriendRequests
from .viewsfolder.author_following_views import AuthorViewFollowing
from.viewsfolder.feed_views import GetAuthorPosts
from .viewsfolder.feed_views import UpdateGithubId
from . import views

urlpatterns = [
    path('users/', UserView.as_view(), name='users'),
    path('author/<pk>/friends', FriendListView.as_view(), name='friendslist'),
    path('followreqs/', FollowReqListView.as_view(), name='followereqlist'),
    path('author/<authorid1>/friends/<authorid2>', AreFriendsView.as_view(), name='arefriends'),
    path('friendrequest/', FriendRequestView.as_view(), name='friendrequest'),
    path('follow/<authorid>/', FollowView.as_view(), name='follow'),
    path('posts/', PostView.as_view(), name='posts'),
    path('frontend/posts/<pk>', FrontEndPostViewID.as_view(), name='frontpostid'),
    path('posts/<pk>', PostViewID.as_view(), name='postid'),
    path('posts/<post_id>/comments/', CommentViewList.as_view(), name='comments'),
    path('frontend/posts/<post_id>/comments/', FrontEndCommentView.as_view(), name='frontcomments'),
    path('users/', UserView.as_view(), name='users'),
    path('author/<pk>/', UserViewID.as_view(), name='author'),
    path('approve/', AdminUserView.as_view(), name='admin-users'),
    path('frontend/user/edit/', FrontEndUserEditView.as_view(), name='edit_user'),
    path('frontend/author/<authorid>/posts', FrontEndAuthorPosts.as_view(), name='frontauthorposts'),
    path('frontend/register/', RegistrationPageView.as_view(), name='register-users'),
    path('frontend/login/', LoginPageView.as_view(), name='login-user'),
    path('frontend/posts/public/', FrontEndPublicPosts.as_view(), name='frontendpublic'),
    path('frontend/posts/feed/', FrontEndFeed.as_view(), name='frontendfeed'),
    path('frontend/posts/create/', PostCreateView.as_view(), name="create_post"),
    path('frontend/friendrequest/<follower>/', AuthorViewFriendRequests.as_view(), name='frontendfriendrequestsdelete'),
    path('frontend/friendrequest/', AuthorViewFriendRequests.as_view(), name='frontendfriendrequests'),
    path('frontend/following/', AuthorViewFollowing.as_view(), name='frontendfollowing'),
    path('author/<authorid>/posts/', GetAuthorPosts.as_view(), name="getAuthorPosts"),
    path('frontend/author/github/', UpdateGithubId.as_view(), name="updateGithubId"),
]
