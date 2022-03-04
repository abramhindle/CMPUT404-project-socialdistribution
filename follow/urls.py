from unicodedata import name
from django.urls import path
from .views import (
    all_users_list,
    create_follow_request,
    accept_follow_request,
    unfollow_request,
    remove_follow_request,
    reject_follow_request
)

app_name = 'follow'
urlpatterns = [
    path('users/', view=all_users_list, name='view_all_users'),
    path('users/request/<slug:to_username>/', view=create_follow_request, name='create_follow_request'),
    path('users/accept/<slug:from_username>', view=accept_follow_request, name='accept_follow_request'),
    path('users/unfollow/<slug:from_username>', view=unfollow_request, name='unfollow_request'),
    path('users/removefollow/<slug:to_username>', view=remove_follow_request, name='remove_follow_request'),
    path('users/reject/<slug:from_username>', view=reject_follow_request, name='reject_follow_request')
]
