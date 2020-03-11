from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Post, Comment
from .forms import CommentForm, PostForm
from django.contrib.auth.decorators import login_required
import base64


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

@login_required
def edit_post(request, post_id):
    author = request.user
    template = 'posts/posts_edit.html'
    post = Post.objects.get(id=post_id)

    form = PostForm(request.POST or None, request.FILES or None,
                       instance=post)

    context = {
        'form': form,
        'author': author,
    }

    if request.method == 'POST':
        if form.is_valid():
            new_content = form.save(commit=False)
            cont_type = form.cleaned_data['content_type']
            if(cont_type == "image/png;base64" or cont_type == "image/jpeg;base64"):
                img = form.cleaned_data['image_file']
                new_content.content = (base64.b64encode(img.file.read())).decode("utf-8")
            print(new_content)
            new_content.save()
            url = reverse('details', kwargs={'post_id': post.id})
            return HttpResponseRedirect(url)


    return render(request, template, context)
