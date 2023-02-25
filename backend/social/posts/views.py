from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse,reverse_lazy
from django.views import generic
from .models import Post
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from django.http import HttpResponse


class IndexView(generic.ListView):
    template_name = 'posts/index.html'
    context_object_name = 'latest_posts'

    def get_queryset(self):
        """Return the last five published posts."""
        return Post.objects.order_by('title')[:5]

class DetailView(generic.DetailView):
    model = Post
    context_object_name = 'postt'
    template_name = 'posts/detail.html'
    

class PostDeleteView(UserPassesTestMixin,LoginRequiredMixin,DeleteView):

    model = Post
    template_name = 'posts/delete.html'
    context_object_name = 'post'
    success_url = '/admin/'
    
    
    def test_func(self):
        post = self.get_object()
        print(post.title)
        if self.request.user == post.author.user:
            return True
        return False
