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

class IndexView(generic.ListView):
    template_name = 'post/index.html'
    context_object_name = 'all_posts'

    def get_queryset(self):
        return Post.objects.all().order_by('-pub_date')

class DetailView(generic.DetailView):
    model = Post
    template_name = 'post/detail.html'

'''
class PostCreate(CreateView):
    model = Post
    fields = ['post_story', 'author']
    success_url = reverse_lazy('post:index')
'''
class PostUpdate(UpdateView):
    model = Post
    fields = ['post_story']

class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('post:index')

@login_required
def post_create(request):

    #print(author.id)

    if not request.user.is_authenticated():
        raise Http404

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = Author.objects.get(request.user.id)
        instance.save()
        messages.success(request, "You just added a new post.")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "post/post_form.html", context)


