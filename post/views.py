import CommonMark
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
from .models import Post, Comment
from .forms import CommentForm
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q


class IndexView(generic.ListView):
    template_name = 'post/index.html'
    context_object_name = 'all_posts'

    def get_queryset(self):
        return Post.objects.all().order_by('-pub_date')


def view_posts(request):
    if request.user.is_authenticated():
        user = request.user
        author = Author.objects.get(user=request.user.id)
        context = dict()
        context1 = dict()
        context2 = dict()

        # NOTE: this does the same thing as the function indexHome in dashboard/view.py
        # Return posts that are NOT by current user (=author) and:

        # case 1: post.visibility=public and following               --> can view
        # case 1': post.visibility=public  and not following          --> can't view
        # case 2': post.visibility=friends and not friends            --> can't view
        context1['visible_posts'] = Post.objects \
            .filter(~Q(author__id=user.profile.id)) \
            .filter(author__id__in=author.followed_authors.all()) \
            .filter(visibility="PUBLIC").order_by('-pub_date')

        # case 2: post.visibility=friends and friends                 --> can view
        context2['visible_posts'] = Post.objects \
            .filter(~Q(author__id=user.profile.id)) \
            .filter(author__id__in=author.friends.all()) \
            .filter(Q(visibility="FRIENDS") | Q(visibility="PUBLIC")).order_by('-pub_date')

        context["visible_posts"] = context1["visible_posts"] | context2["visible_posts"]

        # TODO: need to be able to filter posts by current user's relationship to post author
        # case 3: post.visibility=foaf and friend/foaf                --> can view
        # case 3': post.visibility=foaf and not either friend/foaf    --> can view
        # case 4: post.visibility=private                             --> can't see

        return render(request, 'post/index.html', context)

    else:
        # Return all posts on present on the site
        context = dict()
        context['visible_posts'] = Post.objects.filter(visibility="PUBLIC").order_by('-pub_date')
        return render(request, 'post/index.html', context)


class DetailView(generic.DetailView):
    model = Post
    template_name = 'post/detail.html'


class PostUpdate(UpdateView):
    model = Post
    fields = ['post_story', 'image']


class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('post:index')

def view_post_comments(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = dict()
    context["all_comments"] = Comment.objects.filter(post_id=post.id)
    return render(request, 'post/comments.html', context)

@login_required
def post_create(request):

    if not request.user.is_authenticated():
        raise Http404

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = Author.objects.get(user=request.user.id)
        if instance.use_markdown:
            parser = CommonMark.Parser()
            renderer = CommonMark.HtmlRenderer(options={'safe': True})
            post_story_html = renderer.render(parser.parse(form.cleaned_data['post_story']))
            instance.post_story = post_story_html
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

