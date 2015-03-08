from django.shortcuts import render, redirect, render_to_response
from django.http import HttpRequest
from django.template import RequestContext
from post.models import Post, AuthoredPost, VisibleToAuthor
from author.models import Author



def createPost(request):
    context = RequestContext(request)

    if request.method == "POST":
        if request.user.is_authenticated():
            text = request.POST.get("text_body", "")
            author = Author.objects.get(user=request.user)
            visibility = request.POST.get("visibility_type", "")
            mime_type = "text/plain" # TODO: not sure whether to determine type or have user input type

            new_post = Post.objects.create(text=text, mime_type=mime_type, visibility=visibility)
            AuthoredPost.objects.create(author=author, post=new_post)

            if visibility == Post.ANOTHER_AUTHOR: #TODO: should prob not do this
                try:
                    visible_author = request.POST.get("visible_author", "") #TODO somehow change this to get the actual author
                    visible_author_obj = Author.objects.get(user=visible_author)

                    VisibleToAuthor.objects.create(visibleAuthor=visible_author_obj, post=new_post)
                except Author.DoesNotExist:
                    print("hmm") #TODO: not too sure if care about this enough to handle it
        else:
            return redirect('/login.html', 'Please log in.', context)

    return redirect(index)


# def modifyPost(request):


# def deletePost(request):

def index(request):

    context = RequestContext(request)

    if request.method == 'GET':
        if request.user.is_authenticated():
            try:
                post_instance = Post()
                author = Author.objects.get(user=request.user)
                posts = Post.getByAuthor(author)
                visibility_types = post_instance.getVisibilityTypes()
                return render_to_response('index.html', {'posts':posts, 'visibility':visibility_types}, context)
            except Author.DoesNotExist:
                return _render_error('/login.html', 'Please log in.', context)
        else:
            return _render_error('/login.html', 'Please log in.', context)
    else:
        _render_error('/login.html', 'Invalid request.', context)


# def posts(request):

# def post(request, post_id):

def _render_error(url, error, context):
    context['error'] = error
    return render_to_response(url, context)