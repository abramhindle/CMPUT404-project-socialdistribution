from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from comment.models import Comment
from author.models import Author
from post.models import Post

import uuid


def add_comment(request):
    context = RequestContext(request)

    if request.method == 'POST':
        if request.user.is_authenticated():
            author = Author.objects.get(user=request.user)
            guid = uuid.uuid1()
            comment = request.POST.get("comment", "")
            post = Post.objects.get(guid=request.POST.get("post_id", ""))

            Comment.objects.create(guid=guid,
                                   author=author,
                                   comment=comment,
                                   post=post)
        else:
            loginError(context)


    return HttpResponseRedirect(request.META.get('HTTP_REFERER'), status=302)

def remove_comment(request, comment_id):
    context = RequestContext(request)

    if request.user.is_authenticated():
        Comment.removeComment(comment_id)
    else:
        loginError(context)

    return redirect(request.META.get('HTTP_REFERER'))

def loginError(context):
    _render_error('login.html', 'Please log in.', context)

def _render_error(url, error, context):
    context['error'] = error
    return render_to_response(url, context)