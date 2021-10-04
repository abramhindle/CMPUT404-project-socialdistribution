from django.shortcuts import render
from django.views import generic

# Create your views here.
class PostsView(generic.TemplateView):
    template_name = 'posts.html'