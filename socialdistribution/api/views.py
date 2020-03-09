import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from profiles.models import Author
from posts.models import Post, Comment

from .utils import post_to_dict, comment_to_dict, is_valid_post, insert_post, update_post


# Create your views here.
@csrf_exempt
def posts(request):
    # # this view only accepts GET, 405 Method Not Allowed for other methods
    # if request.method != "GET":
    #     return HttpResponse(f"Method {request.method} not allowed", status=405)

    # get public posts
    if request.method == "GET":
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

    # insert new post
    elif request.method == "POST":
        request_body = json.loads(request.body)

        # post is not va;id - 400 Bad Request or 422 Unprocessable Entity
        if not is_valid_post(request_body):
            return HttpResponse("Invalid post", status=400)

        # valid post --> insert to DB
        post = insert_post(request_body)

        return JsonResponse(post_to_dict(post))

    # insert new post
    elif request.method == "PUT":
        request_body = json.loads(request.body)

        # post is not valid - 400 Bad Request or 422 Unprocessable Entity
        if not is_valid_post(request_body):
            return HttpResponse("Invalid post", status=400)

        # valid post --> insert to DB
        post = insert_post(request_body)

        return JsonResponse(post_to_dict(post))


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

    # PUT a post which exists - update post
    if request.method == "PUT" and posts.count() > 0:
        post_to_update = posts[0]

        request_body = json.loads(request.body)

        # post is not valid - 400 Bad Request or 422 Unprocessable Entity
        if not is_valid_post(request_body):
            return HttpResponse("Invalid post", status=400)

        # valid post --> update existing post
        post = update_post(post_to_update, request_body)

        return JsonResponse(post_to_dict(post))

    # delete a post
    if request.method == "DELETE" and posts.count() > 0:
        post = posts[0]
        post.delete()

        return HttpResponse("Post deleted")

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
