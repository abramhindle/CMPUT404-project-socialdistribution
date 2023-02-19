from django.urls import path
from .views.author import multiple_authors, single_author

urlpatterns = [
    #for every different model, create a new model file and view file in the /model and /view directories then link it up here
    path('', multiple_authors, name='author_request'), 
    path('<uuid:id>/', single_author, name='single_author')
]