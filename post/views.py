'''
from django.shortcuts import render, get_object_or_404
from . models import Post


def index(request):
    all_posts = Post.objects.all()
    context = {
        'all_posts': all_posts,
    }

    return render(request, 'post/index.html', context)

def detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    return render(request, 'post/detail.html', {'post': post})
'''


from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from . models import Post


class IndexView(generic.ListView):
    template_name = 'post/index.html'
    context_object_name = 'all_posts'

    def get_queryset(self):
        return Post.objects.all()

class DetailView(generic.DetailView):
    model = Post
    template_name = 'post/detail.html'


class PostCreate(CreateView):
    model = Post
    fields = ['post_story']
    success_url = reverse_lazy('post:index')

class PostUpdate(UpdateView):
    model = Post
    fields = ['post_story']

class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('post:index')
