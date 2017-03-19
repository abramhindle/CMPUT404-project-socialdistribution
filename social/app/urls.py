from django.conf.urls import url, include

from social.app.views import post as post_views
from social.app.views import author as author_views
from social.app.views import friend as friend_views

posts_urlpatterns = [
    # /posts/
    url(r'^$', post_views.view_posts, name='index'),

    # /posts/71/
    url(r'^(?P<pk>[0-9]+)/$', post_views.DetailView.as_view(), name='detail'),

    # /posts/add/
    url(r'^add/$', post_views.post_create, name='posts-add'),

    # This is to update posts. Currently not set-up in the front-end
    # /posts/71/
    url(r'(?P<pk>[0-9]+)/edit/$', post_views.PostUpdate.as_view(), name='posts-update'),

    # /posts/71/delete/
    url(r'(?P<pk>[0-9]+)/delete/$', post_views.PostDelete.as_view(), name='posts-delete'),

    # /posts/71/comment
    url(r'(?P<pk>[0-9]+)/comment/$', post_views.add_comment_to_post, name='add_comment_to_post'),

    # view all comments on a posts
    # /posts/71/comments
    url(r'(?P<pk>[0-9]+)/comments/$', post_views.view_post_comments, name='view-posts-comments'),
]

authors_urlpatterns = [
    # /authors/
    url(r'^$', author_views.AuthorListView.as_view(), name='list'),
    # /authors/aeea8619-a9c1-4792-a273-80ccb7255ea2/
    url(r'^(?P<pk>[0-9,a-z,\\-]+)$', author_views.AuthorDetailView.as_view(), name='detail'),
    # /authors/aeea8619-a9c1-4792-a273-80ccb7255ea2/posts/
    url(r'^(?P<pk>[0-9,a-z,\\-]+)/posts/$', author_views.view_posts_by_author, name='posts-by-author'),
]

urlpatterns = [
    url(r'^$', post_views.indexHome, name='index'),
    url(r'^dashboard/$', post_views.index, name='dashboard'),
    url(r'^posts/', include(posts_urlpatterns, namespace='posts')),
    url(r'^authors/', include(authors_urlpatterns, namespace='authors')),
    url(r'^friendrequests/$', friend_views.FriendRequestsListView.as_view(), name='friend-requests-list'),
]
