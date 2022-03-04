from django.urls import path
from django.contrib.auth.views import LoginView

from .views import SignUpView, ProfileView

app_name = 'auth_provider'
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('profile/', ProfileView.as_view(), name='user_profile'),
]
