from django.http import HttpResponseRedirect, QueryDict, HttpResponse
from django.shortcuts import redirect, render_to_response, render
from django.template import RequestContext
from category.models import Category,PostCategory

import json

def index(request):
    context = RequestContext(request)
    if request.method == 'DELETE':
        if request.user.is_authenticated():
            PostCategory.removeCatagory(QueryDict(request.body).get('category_id'))
            return HttpResponse(json.dumps({'msg': 'category deleted'}),
                                content_type="application/json")
        else:
            loginError(context)

    elif request.method == 'POST':
        if request.user.is_authenticated():
            return redirect('../../author/posts', context)
        else:
            loginError(context)


def loginError(context):
    _render_error('login.html', 'Please log in.', context)


def _render_error(url, error, context):
    context['error'] = error
    return render_to_response(url, context)

