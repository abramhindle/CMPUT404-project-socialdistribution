from django.http import HttpResponseRedirect, QueryDict, HttpResponse
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.utils import timezone
from comment.models import Comment
from author.models import Author
from post.models import Post

import uuid
import json


def comment(request):
    context = RequestContext(request)

    if request.method == 'DELETE':
        if request.user.is_authenticated():
            Comment.removeComment(QueryDict(request.body).get('comment_id'))
            return HttpResponse(json.dumps({'msg': 'post deleted'}),
                                content_type="application/json")
        else:
            loginError(context)

    elif request.method == 'POST':
        if request.user.is_authenticated():
            author = Author.objects.get(user=request.user)
            guid = uuid.uuid1()
            comment = request.POST.get("comment", "")
            post = Post.objects.get(guid=request.POST.get("post_id", ""))

            new_comment = Comment.objects.create(guid=guid,
                                                 author=author,
                                                 comment=comment,
                                                 post=post,
                                                 pubDate=timezone.now())

            return HttpResponse(json.dumps(new_comment.getJsonObj()),
                                content_type="application/json")
        else:
            loginError(context)

# http://stackoverflow.com/questions/23285558/datetime-date2014-4-25-is-not-json-serializable-in-django
# def dateHandler(obj):
#     return obj.isoformat() if hasattr(obj, 'isoformat') else obj


def loginError(context):
    _render_error('login.html', 'Please log in.', context)


def _render_error(url, error, context):
    context['error'] = error
    return render_to_response(url, context)
