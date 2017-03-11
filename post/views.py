from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from . models import Post
from django.contrib.auth.models import User
from dashboard.models import Author
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
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

class PostUpdate(UpdateView):
    model = Post
    fields = ['post_story', 'image']


class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('post:index')


@login_required
def post_create(request):

    if not request.user.is_authenticated():
        raise Http404

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = Author.objects.get(user=request.user.id)
        instance.save()
        messages.success(request, "You just added a new post.")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "post/post_form.html", context)


# Based on code by Django Girls,
# url: https://djangogirls.gitbooks.io/django-girls-tutorial-extensions/homework_create_more_models/
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = Author.objects.get(user=request.user.id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = user
            comment.post = post
            comment.save()
            return redirect('post:detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'post/add_comment_to_post.html', {'form': form})

