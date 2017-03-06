from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from . models import Post


class IndexView(generic.ListView):
    template_name = 'post/index.html'
    context_object_name = 'all_posts'

    def get_queryset(self):
        return Post.objects.all().order_by('-pub_date')

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
