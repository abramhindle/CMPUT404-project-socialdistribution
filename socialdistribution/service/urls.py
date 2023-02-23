from django.urls import path
from .views.author import SingleAuthor, MultipleAuthors
# from .views.follower_views import FollowerAPIView, FollowersAPIView

urlpatterns = [
    #for every different model, create a new model file and view file in the /model and /view directories then link it up here
    # path('service/authors/<str:author>/followers', FollowersAPIView.as_view(), name='service-followers'),
    # path('service/authors/<str:author>/followers/<str:another_author>', FollowerAPIView.as_view(), name='service-follower'),
    path('', MultipleAuthors.as_view()), 
    path('<uuid:id>/', SingleAuthor.as_view())
]