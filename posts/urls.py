from posts import views
from django.urls import path

app_name = 'posts'
urlpatterns = [
    path('<int:pk>/edit', views.EditPostView.as_view(), name='edit'),
    path('<int:pk>/comments/new', views.CreateCommentView.as_view(), name='new-comment'),
    path('<int:pk>', views.PostDetailView.as_view(), name='detail'),
    path('new', views.CreatePostView.as_view(), name='new'),
    path('', views.MyPostsView.as_view(), name='my-posts'),
    path('<int:pk>/like', views.LikePostView.as_view(), name='like'),
]
