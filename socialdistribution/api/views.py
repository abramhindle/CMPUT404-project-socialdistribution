import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from profiles.models import Author, AuthorFriend
from posts.models import Post, Comment

from .utils import post_to_dict, comment_to_dict, author_to_dict, is_valid_post, insert_post, update_post, is_valid_comment, insert_comment, validate_friend_request


# Create your views here.
@csrf_exempt
def posts(request):
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
    # TODO: authentication
    elif request.method == "POST":
        request_body = json.loads(request.body)

        # post is not va;id - 400 Bad Request or 422 Unprocessable Entity
        if not is_valid_post(request_body):
            return HttpResponse("Invalid post", status=400)

        # valid post --> insert to DB
        post = insert_post(request_body)

        return JsonResponse(post_to_dict(post))

    # insert new post
    # TODO: authentication
    elif request.method == "PUT":
        request_body = json.loads(request.body)

        # post is not valid - 400 Bad Request or 422 Unprocessable Entity
        if not is_valid_post(request_body):
            return HttpResponse("Invalid post", status=400)

        # valid post --> insert to DB
        post = insert_post(request_body)

        return JsonResponse(post_to_dict(post))

    # invalid method
    return HttpResponse(f"Method {request.method} not allowed", status=405)


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
    # TODO: authentication
    if request.method == "GET" and posts.count() > 0:
        response_body = {
            "query" : "posts",
            "post" : post_to_dict(posts[0])
        }

        return JsonResponse(response_body)

    # PUT a post which exists - update post
    # TODO: author as currently authenticated user
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
    # TODO: authenticate
    if request.method == "DELETE" and posts.count() > 0:
        post = posts[0]
        post.delete()

        return HttpResponse("Post deleted")

    
    # invalid method
    return HttpResponse(f"Method {request.method} not allowed", status=405)

@csrf_exempt
def specific_author_posts(request, author_id):
    # this view only accepts GET, 405 Method Not Allowed for other methods
    if request.method != "GET":
        return HttpResponse(f"Method {request.method} not allowed", status=405)

    authors = Author.objects.filter(id=author_id)

    # author does not exist - 404 Not Found
    if authors.count() == 0:
        return HttpResponse("That author does not exist", status=404)

    # TODO: only posts currently authenticated user can see
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
def author_posts(request):
    # this view only accepts GET, 405 Method Not Allowed for other methods
    if request.method != "GET":
        return HttpResponse(f"Method {request.method} not allowed", status=405)

    # TODO: only posts the currently authenticated author can see
    posts = Post.objects.filter(visibility="PUBLIC")

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
    # get comments for the post
    if request.method == "GET":
        # get the post
        posts = Post.objects.filter(id=post_id)

        # TODO: should this only get comments for posts visible to the currently authenticated author?

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

    # post a comment
    elif request.method == "POST":
        request_body = json.loads(request.body)

        # TODO: check if authenticated user can see post
        # authenticated user cannot see this post
        if False:
            response_body = {
                "query": "addComment",
                "success": False,
                "message": "Comment not allowed"
            }

            return JsonResponse(response_body, status=403)

        # comment is not valid - 400 Bad Request or 422 Unprocessable Entity
        if not is_valid_comment(request_body):
            response_body = {
                "query": "addComment",
                "success": False,
                "message": "Invalid comment"
            }

            return JsonResponse(response_body, status=400)

        # check if comment author exists, 404 if not
        authors = Author.objects.filter(url=request_body["comment"]["author"]["id"])
        if authors.count() == 0:
            response_body = {
                "query": "addComment",
                "success": False,
                "message": "Author does not exist"
            }

            return JsonResponse(response_body, status=400)

        # valid post --> insert to DB
        comment = insert_comment(request_body)

        response_body = {
            "query": "addComment",
            "success": True,
            "message": "Comment added"
        }

        return JsonResponse(response_body)

    return HttpResponse(f"Method {request.method} not allowed", status=405)


@csrf_exempt
def friend_request(request):
    if request.method == "POST":
        request_body = json.loads(request.body)

        # check that the friend request is valid
        status = validate_friend_request(request_body)

        # invalid request
        if status != 200:
            response_body = {
                "query": "friendrequest",
                "success": False,
                "message": "Invalid request"
            }
            return JsonResponse(response_body, status=status)

        author = Author.objects.get(id=request_body["author"]["id"])
        friend = Author.objects.get(id=request_body["friend"]["id"])

        friend_req = AuthorFriend(author=author, friend=friend)

        friend_req.save()

        response_body = {
            "query": "friendrequest",
            "success": True,
            "message": "Friend request sent"
        }
        return JsonResponse(response_body)
    
    response_body = {
        "query": "friendrequest",
        "success": False,
        "message": f"Invalid method: {request.method}"
    }
    return JsonResponse(response_body, status=405)


def author_profile(request, author_id):
    if request.method == "GET":
        authors = Author.objects.filter(id=author_id)

        # author does not exist - 404 Not Found
        if authors.count() == 0:
            response_body = {
                "query": "authorProfile",
                "success": False,
                "message": "That author does not exist"
            }
            return JsonResponse(response_body, status=404)

        author = authors[0]

        response_body = author_to_dict(author)

        response_body["friends"] = [
            author_to_dict(friend) for friend in 
        ]

        return JsonResponse(author_to_dict(author))

    response_body = {
        "query": "authorProfile",
        "success": False,
        "message": f"Invalid method: {request.method}"
    }
    return JsonResponse(response_body, status=405)