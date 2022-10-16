from django.urls import path,include
from . import views
from .views import(
    SingleAuthorView,
    AuthorsView,
)

# first argument, endpoint, second argument is the view that calling the url will send the request to

urlpatterns = [
    path('authors',AuthorsView.as_view()),
    path('authors/<int:author_id>/',SingleAuthorView.as_view())
    
]