from django.urls import path
from . import views
from .views import(
    AuthorDetailView,
    AuthorsView,
    AuthorRegistrationView,
    LoginView,
    LogoutView,
    FollowRequestsView,
    FollowRequestDetailView,
    InboxView,
    FollowersDetailView,
    FollowersView,
    PostView,
    AllPosts,
    AllPublicPostsView,
    NodesView,
    NodeDetailView,
    PostLikesView,
    AuthorLikedView
)

# first argument, endpoint, second argument is the view that calling the url will send the request to

urlpatterns = [
    path('authors/', AuthorsView.as_view()),
    path('authors/<str:pk>/', AuthorDetailView.as_view(), name='author-detail'),
    path('register/', AuthorRegistrationView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('nodes/', NodesView.as_view()),
    path('nodes/<str:node_id>/', NodeDetailView.as_view()),
    path('authors/<str:author_id>/follow-requests/', FollowRequestsView.as_view()),
    path('authors/<str:author_id>/follow-requests/<str:foreign_author_id>/', FollowRequestDetailView.as_view()),
    path('authors/<str:author_id>/followers/', FollowersView.as_view()),
    path('authors/<str:author_id>/followers/<str:foreign_author_id>/', FollowersDetailView.as_view()),
    path('authors/<str:author_id>/inbox/', InboxView.as_view()),
    path('authors/<str:pk>/posts/<str:post_id>/',PostView.as_view()),
    path('authors/<str:pk>/posts/',AllPosts.as_view()),
    path('posts/', AllPublicPostsView.as_view()),
    path('authors/<str:pk>/posts/<str:post_id>/likes/',PostLikesView.as_view()),
    path('authors/<str:pk>/liked/',AuthorLikedView.as_view()),
]