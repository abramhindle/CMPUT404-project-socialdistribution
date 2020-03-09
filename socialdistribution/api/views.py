from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from profiles.models import Author
from posts.models import Post, Comment

from .utils import post_to_dict, comment_to_dict


# Create your views here.
@csrf_exempt
def all_posts(request):
    # this view only accepts GET, 405 Method Not Allowed for other methods
    if request.method != "GET":
        return HttpResponse(f"Method {request.method} not allowed", status=405)

    # get a list of all "PUBLIC" visibility posts on our node
    public_posts = Post.objects.filter(visibility='PUBLIC')

    # response body - to be converted into JSON and returned in the response
    response_body = {
        "query" : "posts",
        "count" : public_posts.count(),
        "size"  : "IMPLEMENT PAGINATION",
        "next"  : "IMPLEMENT PAGINATION",
        "previous" : "IMPLEMENT PAGINATION",
        "posts" : [post_to_dict(post) for post in public_posts]
    }

    return JsonResponse(response_body)

@csrf_exempt
def single_post(request, post_id):
    posts = Post.objects.filter(id=post_id)
    
    # GET a post which doesn't exist - 404 Not Found
    if request.method == "GET" and posts.count() == 0:
        return HttpResponse("That post does not exist", status=404)

    # POST (insert) a post which already exists - 403 Forbidden
    if request.method == "POST" and posts.count() > 0:
        return HttpResponse("That post already exists", status=403)

    # GET a post which exists - return post in JSON format
    if request.method == "GET" and posts.count() > 0:
        response_body = {
            "query" : "posts",
            "post" : post_to_dict(posts[0])
        }

        return JsonResponse(response_body)

    # TODO
    # POST / PUT a post which doesn't exist - insert post
    if request.method in ("POST", "PUT") and posts.count() == 0:
        return HttpResponse("Insert post")

    # TODO
    # PUT a post which exists - update post
    if request.method == "PUT" and posts.count() > 0:
        return HttpResponse("Update post")

@csrf_exempt
def author_posts(request, author_id):
    # this view only accepts GET, 405 Method Not Allowed for other methods
    if request.method != "GET":
        return HttpResponse(f"Method {request.method} not allowed", status=405)

    authors = Author.objects.filter(id=author_id)

    # author does not exist - 404 Not Found
    if authors.count() == 0:
        return HttpResponse("That author does not exist", status=404)

    posts = Post.objects.filter(author=authors[0])

    response_body = {
        "query": "posts",
        "count": posts.count(),
        "size": "IMPLEMENT PAGINATION",
        "next": "IMPLEMENT PAGINATION",
        "previous": "IMPLEMENT PAGINATION",
        "posts": [post_to_dict(post) for post in posts]
    }

    return JsonResponse(response_body)

@csrf_exempt
def post_comments(request, post_id):
    # this view only accepts GET, 405 Method Not Allowed for other methods
    if request.method != "GET":
        return HttpResponse(f"Method {request.method} not allowed", status=405)

    # get the post
    posts = Post.objects.filter(id=post_id)

    # post does not exist - 404 Not Found
    if posts.count() == 0:
        return HttpResponse("That post does not exist", status=404)

    # get the comments for the post
    comments = Comment.objects.filter(post=posts[0])

    response_body = {
        "query": "comments",
        "count": comments.count(),
        "size": "IMPLEMENT PAGINATION",
        "next": "IMPLEMENT PAGINATION",
        "previous": "IMPLEMENT PAGINATION",
        "comments": [comment_to_dict(comment) for comment in comments]
    }

    return JsonResponse(response_body)
