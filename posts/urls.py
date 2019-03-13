from django.urls import path
from .views import AdminUserView
from .views import UserView, PostView, PostViewID, FrontEndPostViewID, CommentViewList
from .viewsfolder.login_reg_view import RegistrationPageView, LoginPageView
urlpatterns = [
    path('posts/', PostView.as_view(), name='posts'),
    path('frontend/posts/<pk>', FrontEndPostViewID.as_view(), name='frontpostid'),
    path('posts/<pk>', PostViewID.as_view(), name='postid'),
    path('posts/<post_id>/comments/', CommentViewList.as_view(), name='comments'),
    path('users/', UserView.as_view(), name='users'),
    path('approve/', AdminUserView.as_view(), name='admin-users'),
    path('register/', RegistrationPageView.as_view(), name='register-users'),
    path('frontend/login', LoginPageView.as_view(), name='login-user')
]
