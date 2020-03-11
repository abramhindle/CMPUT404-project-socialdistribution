from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Post, Comment
from .forms import CommentForm
from django.contrib.auth.decorators import login_required


@login_required
def index(request):

    author = request.user
    template = 'posts/posts_base.html'
    latest_post_list = Post.objects.filter(visibility='PUBLIC', unlisted=False).order_by('-published')
    context = {
        'latest_post_list': latest_post_list,
        'author': author,
    }

    return render(request, template, context)


@login_required
def post_comments(request, post_id):
    return HttpResponse("You are looking at the comments of post %s. " % post_id)


@login_required
def view_post(request, post_id):
    author = request.user
    template = 'posts/posts_view.html'
    post = Post.objects.get(id=post_id)
    latest_post_list = Post.objects.order_by('-published')[:5]
    comments = Comment.objects.filter(post=post).order_by('published')

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('comment')
            comment = Comment.objects.create(post=post, author=author, comment=content)
            comment.save()
            return HttpResponseRedirect(request.path_info)
        # What should we do if the form is invalid?
    else:
        comment_form = CommentForm()

    context = {
        'latest_post_list': latest_post_list,
        'author': author,
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }

    return render(request, template, context)
