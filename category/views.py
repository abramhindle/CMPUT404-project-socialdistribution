from django.http import HttpResponseRedirect, QueryDict, HttpResponse
from django.shortcuts import redirect, render_to_response, render
from django.template import RequestContext
from comment.models import Comment
from author.models import Author
from post.models import Post
from category.models import Category,PostCategory

import uuid
import json
def index(request):
    context=RequestContext(request)
    post=PostCategory.objects.all()
    return render_to_response('test.html',{'post':post},context)

def category(request,category_name):
    context =RequestContext(request)
    the_category= Category.objects.get(name=category_name)
    categories= the_category.link_set.all()
    return render_to_response('test.html', {'categories':categories,'category_name':'#'+category_name},context)

def categories(request):
    context = RequestContext(request)
    categories = Category.objects.all()
    return render_to_response('category.html', {'categories':categories}, context)

def postcategory(request):
    context = RequestContext(request)
    if request.method == 'DELETE':
        if request.user.is_authenticated():
            Category.removeCatagory(QueryDict(request.body).get('category_id'))
            return HttpResponse(json.dumps({'msg': 'post deleted'}),
                                content_type="application/json")
        else:
            loginError(context)

    elif request.method == 'POST':
        if request.user.is_authenticated():
            title = request.POST.get("title", "")
            description = request.POST.get("description", "")
            content = request.POST.get("text_body", "")
            author = Author.objects.get(user=request.user)
            visibility = request.POST.get("visibility_type", "")
            content_type = Post.MARK_DOWN if request.POST.get("markdown_checkbox", False) else Post.PLAIN_TEXT        
            category = request.POST.get("category", "")
            author = Author.objects.get(user=request.user)
            guid = uuid.uuid1()
            obj = None
            created = False
            #post = Post.objects.get(guid=request.POST.get("post_id", ""))
            new_post = PostCategory.objects.create(title=title,
                                               description=description,
                                               guid=guid,
                                               content=content,
                                               content_type=content_type,
                                               visibility=visibility,
                                               author=author)
            tagA = category.split(r'; |, ') 
            for tag in tagA:
                print(tag)
                obj, created = Category.objects.get_or_create(name=tag.lower())
                if created:
                    context['message'] = "%s added to Dogenode!" % obj
                else:
                    context['message'] = "%s already exists!" % obj
                new_post.categories.add(obj)
            return redirect('../../author/posts', context)
        else:
            loginError(context)


def loginError(context):
    _render_error('login.html', 'Please log in.', context)


def _render_error(url, error, context):
    context['error'] = error
    return render_to_response(url, context)

