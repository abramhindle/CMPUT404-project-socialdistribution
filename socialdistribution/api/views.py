from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from profiles.models import Author, AuthorFriend
from posts.models import Post, Comment
from profiles.utils import getFriendsOfAuthor
from .utils import (
    post_to_dict,
    comment_to_dict,
    author_to_dict,
    is_valid_post,
    insert_post,
    update_post,
    is_valid_comment,
    insert_comment,
    validate_friend_request,
    author_can_see_post,
)

import json


# Create your views here.
@csrf_exempt
def posts(request):
    # get public posts
    if request.method == "GET":
        # get a list of all "PUBLIC" visibility posts on our node
        public_posts = Post.objects.filter(visibility="PUBLIC")

        # response body - to be converted into JSON and returned in the response
        response_body = {
            "query": "posts",
            "count": public_posts.count(),
            "size": "IMPLEMENT PAGINATION",
            "next": "IMPLEMENT PAGINATION",
            "previous": "IMPLEMENT PAGINATION",
            "posts": [post_to_dict(post) for post in public_posts],
        }

        return JsonResponse(response_body)

    # insert new post
    elif request.method == "POST":
        request_body = json.loads(request.body)

        # post is not valid - 400 Bad Request or 422 Unprocessable Entity
        if not is_valid_post(request_body):
            response_body = {
                "query": "posts",
                "success": False,
                "message": "Invalid post",
            }
            return JsonResponse(response_body, status=400)

        author = Author.objects.get(id=request_body["author"]["id"])
        # wrong author
        if author != request.user:
            response_body = {
                "query": "posts",
                "success": False,
                "message": "Must login to post",
            }
            return JsonResponse(response_body, status=403)

        if "id" in request_body.keys():
            posts = Post.objects.filter(id=request_body["id"])
            # post already exists
            if posts.count() > 0:
                response_body = {
                    "query": "posts",
                    "success": False,
                    "message": "Post already exists",
                }
                return JsonResponse(response_body, status=400)        

        # valid post --> insert to DB
        post = insert_post(request_body)

        return JsonResponse(post_to_dict(post))

    # insert new post
    # note: PUT requires an ID whereas POST does not
    elif request.method == "PUT":
        request_body = json.loads(request.body)

        # post is not valid - 400 Bad Request or 422 Unprocessable Entity
        if not is_valid_post(request_body):
            response_body = {
                "query": "posts",
                "success": False,
                "message": "Invalid post",
            }
            return JsonResponse(response_body, status=400)

        author = Author.objects.get(id=request_body["author"]["id"])
        # wrong author
        if author != request.user:
            response_body = {
                "query": "posts",
                "success": False,
                "message": "Must login to post",
            }
            return JsonResponse(response_body, status=403)

        if "id" in request_body.keys():
            posts = Post.objects.filter(id=request_body["id"])
            # post already exists
            if posts.count() > 0:
                response_body = {
                    "query": "posts",
                    "success": False,
                    "message": "Post already exists",
                }
                return JsonResponse(response_body, status=400)    
        else:
            response_body = {
                "query": "posts",
                "success": False,
                "message": "Missing post id",
            }
            return JsonResponse(response_body, status=400)    

        # valid post --> insert to DB
        post = insert_post(request_body)

        return JsonResponse(post_to_dict(post))

    # invalid method
    response_body = {
        "query": "posts",
        "success": False,
        "message": f"Invalid method: {request.method}",
    }
    return JsonResponse(response_body, status=405)


@csrf_exempt
def single_post(request, post_id):
    posts = Post.objects.filter(id=post_id)

    if posts.count() > 0:
        if not author_can_see_post(request.user, posts[0]):
            response_body = {
                "query": "posts",
                "success": False,
                "message": "You don't have permission to access that post",
            }
            return JsonResponse(response_body, status=403)

    # GET a post which doesn't exist - 404 Not Found
    if request.method == "GET" and posts.count() == 0:
        response_body = {
            "query": "posts",
            "success": False,
            "message": "Post does not exist",
        }
        return JsonResponse(response_body, status=404)

    # POST (insert) a post which already exists - 403 Forbidden
    if request.method == "POST" and posts.count() > 0:
        response_body = {
            "query": "posts",
            "success": False,
            "message": "Post already exists",
        }
        return JsonResponse(response_body, status=400)

    # GET a post which exists - return post in JSON format
    if request.method == "GET" and posts.count() > 0:
        response_body = {
            "query": "posts", 
            "post": post_to_dict(posts[0])
        }

        return JsonResponse(response_body)

    # PUT a post which exists - update post
    if request.method == "PUT" and posts.count() > 0:
        post_to_update = posts[0]

        if post_to_update.author != request.user:
            response_body = {
                "query": "posts",
                "success": False,
                "message": "You don't have permission to access that post",
            }
            return JsonResponse(response_body, status=403)

        request_body = json.loads(request.body)

        # post is not valid - 400 Bad Request or 422 Unprocessable Entity
        if not is_valid_post(request_body):
            response_body = {
                "query": "posts",
                "success": False,
                "message": "Invalid post",
            }
            return JsonResponse(response_body, status=400)

        # valid post --> update existing post
        post = update_post(post_to_update, request_body)

        return JsonResponse(post_to_dict(post))

    # delete a post
    if request.method == "DELETE" and posts.count() > 0:
        post = posts[0]

        if post.author != request.user:
            response_body = {
                "query": "posts",
                "success": False,
                "message": "You don't have permission to access that post",
            }
            return JsonResponse(response_body, status=403)

        post.delete()

        response_body = {
            "query": "posts",
            "success": True,
            "message": "Post deleted",
        }
        return JsonResponse(response_body, status=403)

    # invalid method
    response_body = {
        "query": "posts",
        "success": False,
        "message": f"Invalid method: {request.method}",
    }
    return JsonResponse(response_body, status=405)


@csrf_exempt
def specific_author_posts(request, author_id):
    # this view only accepts GET, 405 Method Not Allowed for other methods
    if request.method != "GET":
        response_body = {
            "query": "posts",
            "success": False,
            "message": f"Invalid method: {request.method}",
        }
        return JsonResponse(response_body, status=405)

    authors = Author.objects.filter(id=author_id)

    # author does not exist - 404 Not Found
    if authors.count() == 0:
            response_body = {
                "query": "posts",
                "success": False,
                "message": "That author does not exist",
            }
            return JsonResponse(response_body, status=404)

    # TODO: make this faster
    visible_posts = []
    for post in Post.objects.filter(author=authors[0]):
        if author_can_see_post(request.user, post):
            visible_posts.append(post)

    response_body = {
        "query": "posts",
        "count": len(visible_posts),
        "size": "IMPLEMENT PAGINATION",
        "next": "IMPLEMENT PAGINATION",
        "previous": "IMPLEMENT PAGINATION",
        "posts": [post_to_dict(post) for post in visible_posts],
    }

    return JsonResponse(response_body)


@csrf_exempt
def author_posts(request):
    # this view only accepts GET, 405 Method Not Allowed for other methods
    if request.method != "GET":
        response_body = {
            "query": "posts",
            "success": False,
            "message": f"Invalid method: {request.method}",
        }
        return JsonResponse(response_body, status=405)

    # TODO: make this faster
    visible_posts = []
    for post in Post.objects.all():
        if author_can_see_post(request.user, post):
            visible_posts.append(post)

    response_body = {
        "query": "posts",
        "count": len(visible_posts),
        "size": "IMPLEMENT PAGINATION",
        "next": "IMPLEMENT PAGINATION",
        "previous": "IMPLEMENT PAGINATION",
        "posts": [post_to_dict(post) for post in visible_posts],
    }

    return JsonResponse(response_body)


@csrf_exempt
def post_comments(request, post_id):
    # get the post
    posts = Post.objects.filter(id=post_id)

    # post does not exist - 404 Not Found
    if posts.count() == 0:
        response_body = {
            "query": "comments",
            "success": False,
            "message": "Post does not exist",
        }
        return JsonResponse(response_body, status=404)

    post = posts[0]

    if not author_can_see_post(request.user, post):
        response_body = {
            "query": "comments",
            "success": False,
            "message": "You don't have permission to see that post",
        }
        return JsonResponse(response_body, status=403)

    # get comments for the post
    if request.method == "GET":
        # get the comments for the post
        comments = Comment.objects.filter(post=post)

        response_body = {
            "query": "comments",
            "count": comments.count(),
            "size": "IMPLEMENT PAGINATION",
            "next": "IMPLEMENT PAGINATION",
            "previous": "IMPLEMENT PAGINATION",
            "comments": [comment_to_dict(comment) for comment in comments],
        }

        return JsonResponse(response_body)

    # post a comment
    elif request.method == "POST":
        if request.user.is_anonymous:
            response_body = {
                "query": "addComment",
                "success": False,
                "message": "You must login to post a comment",
            }
            return JsonResponse(response_body, status=403)

        request_body = json.loads(request.body)

        # comment is not valid - 400 Bad Request or 422 Unprocessable Entity
        if not is_valid_comment(request_body):
            response_body = {
                "query": "addComment",
                "success": False,
                "message": "Invalid comment",
            }

            return JsonResponse(response_body, status=400)

        # check if comment author exists, 404 if not
        authors = Author.objects.filter(
            id=request_body["comment"]["author"]["id"])
        if authors.count() == 0:
            response_body = {
                "query": "addComment",
                "success": False,
                "message": "Author does not exist",
            }
            return JsonResponse(response_body, status=404)

        author = authors[0]

        if author != request.user:
            response_body = {
                "query": "addComment",
                "success": False,
                "message": "Cannot post a comment from somebody else's account",
            }
            return JsonResponse(response_body, status=403)

        # valid post --> insert to DB
        comment = insert_comment(post, request_body)

        response_body = {
            "query": "addComment",
            "success": True,
            "message": "Comment added",
        }
        return JsonResponse(response_body)

    response_body = {
        "query": "comments",
        "success": False,
        "message": f"Invalid method: {request.method}",
    }
    return JsonResponse(response_body, status=405)


@csrf_exempt
def friend_request(request):
    if request.method == "POST":
        # ensure user is authenticated
        if request.user.is_anonymous:
            response_body = {
                "query": "friendrequest",
                "success": False,
                "message": "Must be authenticated to send a friend request",
            }
            return JsonResponse(response_body, status=403)

        request_body = json.loads(request.body)

        # check that the friend request is valid
        status = validate_friend_request(request_body)

        # invalid request
        if status != 200:
            response_body = {
                "query": "friendrequest",
                "success": False,
                "message": "Invalid request",
            }
            return JsonResponse(response_body, status=status)

        author = Author.objects.get(id=request_body["author"]["id"])
        friend = Author.objects.get(id=request_body["friend"]["id"])

        # make sure authenticated user is the one sending the friend request
        if author != request.user:
            response_body = {
                "query": "friendrequest",
                "success": False,
                "message": "Cannot send a friend request for somebody else",
            }
            return JsonResponse(response_body, status=403)

        friend_req = AuthorFriend(author=author, friend=friend)

        friend_req.save()

        response_body = {
            "query": "friendrequest",
            "success": True,
            "message": "Friend request sent",
        }
        return JsonResponse(response_body)

    response_body = {
        "query": "friendrequest",
        "success": False,
        "message": f"Invalid method: {request.method}",
    }
    return JsonResponse(response_body, status=405)


@csrf_exempt
def author_profile(request, author_id):
    if request.method == "GET":
        authors = Author.objects.filter(id=author_id)

        # author does not exist - 404 Not Found
        if authors.count() == 0:
            response_body = {
                "query": "authorProfile",
                "success": False,
                "message": "That author does not exist",
            }
            return JsonResponse(response_body, status=404)

        author = authors[0]

        response_body = author_to_dict(author)

        response_body["friends"] = [
            author_to_dict(friend.friend) for friend in getFriendsOfAuthor(author)
        ]

        return JsonResponse(response_body)

    response_body = {
        "query": "authorProfile",
        "success": False,
        "message": f"Invalid method: {request.method}",
    }
    return JsonResponse(response_body, status=405)


@csrf_exempt
def who_am_i(request):
    response_body = {"query": "whoami", "success": True}

    if request.user.is_anonymous:
        response_body["author"] = "Anonymous user (unauthenticated)"
    else:
        response_body["author"] = author_to_dict(request.user)

    return JsonResponse(response_body)


@csrf_exempt
def can_see(request, author_id, post_id):
    author = Author.objects.get(id=author_id)
    post = Post.objects.get(id=post_id)

    if author_can_see_post(author, post):
        return JsonResponse({"cansee": True})
    else:
        return JsonResponse({"cansee": False})
