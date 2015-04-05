from django.conf.urls import patterns, url

from author import views

urlpatterns = patterns(
    'author.views',

    url(r'^$', 'login', name='login'),
    url(r'^register/$', 'register', name='register'),
    url(r'^author/logout/$', views.logout),

    url(r'^author/profile/$', views.profile_self),
    url(r'^author/search/$', views.search),
    url(r'^author/(?P<author_id>[-\w]+)/$', views.profile, name='user_profile'),

    url(r'^author/friends/new$', views.request_friendship,
        name='request_friendship'),
    url(r'^author/friends/accept$', views.accept_friendship,
        name='accept_friendship'),
    url(r'^author/friends/reject$', views.reject_friendship,
        name='reject_friendship'),
    url(r'^author/friends/unfriend$', views.unfriend,
        name='unfriend'),
    url(r'^author/friends/follow$', views.follow,
        name='follow'),
    url(r'^author/(?P<author>[-\w]+)/FriendRequests$',
        views.friend_request_list, name='friend_request_list'),
    url(r'^author/(?P<author>[-\w]+)/Friends$',
        views.friend_list, name='friend_list'),
)
