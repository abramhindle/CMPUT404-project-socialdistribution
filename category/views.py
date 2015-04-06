from django.http import QueryDict, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from author.models import Author
from category.models import PostCategory
from post.models import Post

import json


def index(request):
    context = RequestContext(request)
    if request.method == 'DELETE':
        if request.user.is_authenticated():
            category = QueryDict(request.body).get('category_name')
            post_id = QueryDict(request.body).get('post_id')

            try:
                post = Post.objects.get(guid=post_id)
                PostCategory.removeCategory(post, category, Author.get_author_with_username(request.user.username))

                return HttpResponse(json.dumps({'msg': 'category deleted'}),
                                    content_type="application/json",
                                    status=200)
            except Exception as e:
                return HttpResponse(e.message,
                                    content_type="text/plain",
                                    status=400)

        else:
            loginError(context)

    elif request.method == 'POST':
        if request.user.is_authenticated():
            category = QueryDict(request.body).get('category_name')
            post_id = QueryDict(request.body).get('post_id')

            try:
                post = Post.objects.get(guid=post_id)
                PostCategory.addCategoryToPost(post, category)

                return HttpResponse(json.dumps({'msg': 'category added'}),
                                    content_type="application/json")
            except Exception as e:
                return HttpResponse(e.message,
                                    content_type="text/plain",
                                    status=400)
        else:
            loginError(context)


def loginError(context):
    _render_error('login.html', 'Please log in.', context)


def _render_error(url, error, context):
    context['error'] = error
    return render_to_response(url, context)
