from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import Post
from .forms import CommentForm
from django.shortcuts import render, get_object_or_404, redirect


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
    fields = ['post_story', 'image']
    success_url = reverse_lazy('post:index')


class PostUpdate(UpdateView):
    model = Post
    fields = ['post_story', 'image']


class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('post:index')


# Based on code by Django Girls,
# url: https://djangogirls.gitbooks.io/django-girls-tutorial-extensions/homework_create_more_models/
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post:detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'post/add_comment_to_post.html', {'form': form})
