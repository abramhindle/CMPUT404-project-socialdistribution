from django.urls import path
from .views import UserView,FriendListView

urlpatterns = [
    path('users/', UserView.as_view(), name='users'),
    path('authors/<pk>/friends', FriendListView.as_view(), name='friends')
]