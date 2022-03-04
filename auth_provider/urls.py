from django.urls import path
from django.contrib.auth.views import LoginView

from .views import ProfileView, SignUpView, MyProfileView, EditProfileView, logout_view

app_name = 'auth_provider'
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('<int:pk>', ProfileView.as_view(), name='profile'),
    path('profile/edit', EditProfileView.as_view(), name='edit_profile'),
    path('profile/', MyProfileView.as_view(), name='my_profile'),
]
