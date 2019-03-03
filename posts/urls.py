from django.urls import path
from .views import UserView, AdminUserView

urlpatterns = [
    path('users/', UserView.as_view(), name='users'),
    path('users/approve', AdminUserView.as_view(), name='admin-users')
]