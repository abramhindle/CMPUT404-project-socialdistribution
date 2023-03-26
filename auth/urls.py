from django.urls import path
from .views import CreateUserView

urlpatterns = [
    path('register/', CreateUserView.as_view(), name='register'),
]   