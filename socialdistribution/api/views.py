from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.urls import reverse

from .decorators import check_auth

from urllib import parse
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
    validate_author_friends_post_query,
)

import json


@csrf_exempt
@check_auth
def posts(request):
    # get public posts
    if request.method == "GET":
        # get a list of all "PUBLIC" visibility posts on our node
        public_posts = Post.objects.filter(visibility="PUBLIC").order_by('-published')

        # page number query parameter
        page_number = request.GET.get("page")
        if page_number is None:
            page_number = 0
        else:
            page_number = int(page_number)

        # page size query parameter
        page_size = request.GET.get("size")
        if page_size is None:
            page_size = 50
        else:
            page_size = int(page_size)

        # bad page size
        if page_size <= 0:
            response_body = {
                "query": "posts",
                "success": False,
                "message": "Page size must be a positive integer",
            }
            return JsonResponse(response_body, status=400)

        # paginates our QuerySet
        paginator = Paginator(public_posts, page_size)

        # bad page number
        if page_number < 0 or page_number >= paginator.num_pages:
            response_body = {
                "query": "posts",
                "success": False,
                "message": "That page does not exist",
            }
            return JsonResponse(response_body, status=404)

        # get the page
        # note: the off-by-ones here are because Paginator is 1-indexed 
        # and the example article responses are 0-indexed
        page_obj = paginator.page(str(int(page_number) + 1))

        # response body - to be converted into JSON and returned in response
        response_body = {
            "query": "posts",
            "count": paginator.count,
            "size": int(page_size),
            "posts": [post_to_dict(post, request) for post in page_obj],
        }

        # give a url to the next page if it exists
        if page_obj.has_next():
            next_uri = f"/api/posts?page={page_obj.next_page_number() - 1}&size={page_size}"
            response_body["next"] = request.build_absolute_uri(next_uri)

        # give a url to the previous page if it exists
        if page_obj.has_previous():
            previous_uri = f"/api/posts?page={page_obj.previous_page_number() - 1}&size={page_size}"
            response_body["previous"] = request.build_absolute_uri(previous_uri)

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

        return JsonResponse(post_to_dict(post, request))

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

        return JsonResponse(post_to_dict(post, request))

    # invalid method
    response_body = {
        "query": "posts",
        "success": False,
        "message": f"Invalid method: {request.method}",
    }
    return JsonResponse(response_body, status=405)


@check_auth
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
            "post": post_to_dict(posts[0], request)
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

        return JsonResponse(post_to_dict(post, request))

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
        return JsonResponse(response_body)

    if request.method not in ["GET", "PUT", "DELETE", "POST"]:
        # invalid method
        response_body = {
            "query": "posts",
            "success": False,
            "message": f"Invalid method: {request.method}",
        }
        return JsonResponse(response_body, status=405)


@check_auth
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

    author = authors[0]
    author_posts = Post.objects.filter(author=author)

    # get only visible posts
    visible_post_ids = [post.id for post in author_posts if author_can_see_post(request.user, post)]
    visible_author_posts = author_posts.filter(id__in=visible_post_ids).order_by('-published')

    # page number query parameter
    page_number = request.GET.get("page")
    if page_number is None:
        page_number = 0
    else:
        page_number = int(page_number)

    # page size query parameter
    page_size = request.GET.get("size")
    if page_size is None:
        page_size = 50
    else:
        page_size = int(page_size)

    # bad page size
    if page_size <= 0:
        response_body = {
            "query": "posts",
            "success": False,
            "message": "Page size must be a positive integer",
        }
        return JsonResponse(response_body, status=400)

    # paginates our QuerySet
    paginator = Paginator(visible_author_posts, page_size)

    # bad page number
    if page_number < 0 or page_number >= paginator.num_pages:
        response_body = {
            "query": "posts",
            "success": False,
            "message": "That page does not exist",
        }
        return JsonResponse(response_body, status=404)

    # get the page
    # note: the off-by-ones here are because Paginator is 1-indexed 
    # and the example article responses are 0-indexed
    page_obj = paginator.page(str(int(page_number) + 1))

    # response body - to be converted into JSON and returned in response
    response_body = {
        "query": "posts",
        "count": paginator.count,
        "size": int(page_size),
        "posts": [post_to_dict(post, request) for post in page_obj],
    }

    # give a url to the next page if it exists
    if page_obj.has_next():
        next_uri = f"/api/author/{author.id}/posts?page={page_obj.next_page_number() - 1}&size={page_size}"
        response_body["next"] = request.build_absolute_uri(next_uri)

    # give a url to the previous page if it exists
    if page_obj.has_previous():
        previous_uri = f"/api/author/{author.id}/posts?page={page_obj.previous_page_number() - 1}&size={page_size}"
        response_body["previous"] = request.build_absolute_uri(previous_uri)

    return JsonResponse(response_body)


@check_auth
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

    posts = Post.objects.all()

    # get only visible posts
    visible_post_ids = [post.id for post in posts if author_can_see_post(request.user, post)]
    visible_posts = posts.filter(id__in=visible_post_ids).order_by('-published')

    # page number query parameter
    page_number = request.GET.get("page")
    if page_number is None:
        page_number = 0
    else:
        page_number = int(page_number)

    # page size query parameter
    page_size = request.GET.get("size")
    if page_size is None:
        page_size = 50
    else:
        page_size = int(page_size)

    # bad page size
    if page_size <= 0:
        response_body = {
            "query": "posts",
            "success": False,
            "message": "Page size must be a positive integer",
        }
        return JsonResponse(response_body, status=400)

    # paginates our QuerySet
    paginator = Paginator(visible_posts, page_size)

    # bad page number
    if page_number < 0 or page_number >= paginator.num_pages:
        response_body = {
            "query": "posts",
            "success": False,
            "message": "That page does not exist",
        }
        return JsonResponse(response_body, status=404)

    # get the page
    # note: the off-by-ones here are because Paginator is 1-indexed 
    # and the example article responses are 0-indexed
    page_obj = paginator.page(str(int(page_number) + 1))

    # response body - to be converted into JSON and returned in response
    response_body = {
        "query": "posts",
        "count": paginator.count,
        "size": int(page_size),
        "posts": [post_to_dict(post, request) for post in page_obj],
    }

    # give a url to the next page if it exists
    if page_obj.has_next():
        next_uri = f"/api/author/posts?page={page_obj.next_page_number() - 1}&size={page_size}"
        response_body["next"] = request.build_absolute_uri(next_uri)

    # give a url to the previous page if it exists
    if page_obj.has_previous():
        previous_uri = f"/api/author/posts?page={page_obj.previous_page_number() - 1}&size={page_size}"
        response_body["previous"] = request.build_absolute_uri(previous_uri)

    return JsonResponse(response_body)


@check_auth
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
        comments = Comment.objects.filter(post=post).order_by('-published')

        # page number query parameter
        page_number = request.GET.get("page")
        if page_number is None:
            page_number = 0
        else:
            page_number = int(page_number)

        # page size query parameter
        page_size = request.GET.get("size")
        if page_size is None:
            page_size = 50
        else:
            page_size = int(page_size)

        # bad page size
        if page_size <= 0:
            response_body = {
                "query": "comments",
                "success": False,
                "message": "Page size must be a positive integer",
            }
            return JsonResponse(response_body, status=400)

        # paginates our QuerySet
        paginator = Paginator(comments, page_size)

        # bad page number
        if page_number < 0 or page_number >= paginator.num_pages:
            response_body = {
                "query": "comments",
                "success": False,
                "message": "That page does not exist",
            }
            return JsonResponse(response_body, status=404)

        # get the page
        # note: the off-by-ones here are because Paginator is 1-indexed 
        # and the example article responses are 0-indexed
        page_obj = paginator.page(str(int(page_number) + 1))

        # response body - to be converted into JSON and returned in response
        response_body = {
            "query": "comments",
            "count": paginator.count,
            "size": int(page_size),
            "posts": [comment_to_dict(comment) for comment in page_obj],
        }

        # give a url to the next page if it exists
        if page_obj.has_next():
            next_uri = f"/api/posts/{post.id}/comments?page={page_obj.next_page_number() - 1}&size={page_size}"
            response_body["next"] = request.build_absolute_uri(next_uri)

        # give a url to the previous page if it exists
        if page_obj.has_previous():
            previous_uri = f"/api/posts/{post.id}/comments?page={page_obj.previous_page_number() - 1}&size={page_size}"
            response_body["previous"] = request.build_absolute_uri(previous_uri)

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
                "message": "Cannot post comment from somebody else's account",
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
@check_auth
def author_friends(request, author_uuid):
    # this view only accepts GET, and POSTS,
    # 405 Method Not Allowed for other methods
    if request.method != "GET" and request.method != "POST":
        response_body = {
            "query": "friends",
            "success": False,
            "message": f"Invalid method: {request.method}",
        }
        return JsonResponse(response_body, status=405)

    author = Author.objects.filter(id=author_uuid)
    # author does not exist - 404 Not Found
    if author.count() == 0:
        response_body = {
                "query": "friends",
                "success": False,
                "message": "That author does not exist",
            }
        return JsonResponse(response_body, status=404)

    author = author[0]
    author_friends = getFriendsOfAuthor(author)

    if request.method == "GET":
        author_friends_urls = [
            author_friend.friend.url for author_friend in author_friends
        ]
        response_body = {
            "query": "friends",
            "authors": author_friends_urls,
        }
        return JsonResponse(response_body)

    elif request.method == "POST":
        request_body = json.loads(request.body)
        status = validate_author_friends_post_query(request_body)
        # invalid request
        if status != 200:
            response_body = {
                "query": "friends",
                "success": False,
                "message": "Invalid request",
            }
            return JsonResponse(response_body, status=status)

        # full URL of author, not just id
        request_body_author = request_body['author']
        if author.url != request_body_author:
            response_body = {
                "query": "friends",
                "success": False,
                "message": "Bad request",
            }
            return JsonResponse(response_body, status=400)

        author_friends_urls = [
            author_friend.friend.url for author_friend in author_friends
        ]
        request_body_authors = request_body['authors']

        response_body = {
            "query": "friends",
            "author": author.url,
            "authors": [
                author_url
                for author_url in request_body_authors
                if author_url in author_friends_urls
            ]
        }

        return JsonResponse(response_body)

    response_body = {
        "query": "friends",
        "success": False,
        "message": "Internal server error",
    }

    return JsonResponse(response_body, status=500)


@check_auth
@csrf_exempt
def author_friends_with_author(request, author_uuid, author_friend_url):
    # this view only accepts GET,
    # 405 Method Not Allowed for other methods
    if request.method != "GET":
        response_body = {
            "query": "friends",
            "success": False,
            "message": f"Invalid method: {request.method}",
        }
        return JsonResponse(response_body, status=405)

    author = Author.objects.filter(id=author_uuid)
    # author does not exist - 404 Not Found
    if author.count() == 0:
        response_body = {
                "query": "friends",
                "success": False,
                "message": "That author does not exist",
            }
        return JsonResponse(response_body, status=404)

    author = author[0]
    author_friends = getFriendsOfAuthor(author)

    if request.method == "GET":
        author_friend_url_cleaned = parse.unquote(author_friend_url)
        author_friends_urls = [
            author_friend.friend.url for author_friend in author_friends
        ]
        friends = False
        for url in author_friends_urls:
            if author_friend_url_cleaned in url:
                friends = True
                break
        response_body = {
            "query": "friends",
            "authors": [author.url, author_friend_url_cleaned],
            "friends": friends,
        }

        return JsonResponse(response_body)

    response_body = {
        "query": "friends",
        "success": False,
        "message": "Internal server error",
    }

    return JsonResponse(response_body, status=500)


@check_auth
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


@check_auth
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
        response_body["id"] = author_to_dict(author)["url"]

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


@check_auth
@csrf_exempt
def who_am_i(request):
    response_body = {"query": "whoami", "success": True}

    if request.user.is_anonymous:
        response_body["author"] = "Anonymous user (unauthenticated)"
    else:
        response_body["author"] = author_to_dict(request.user)

    return JsonResponse(response_body)


@check_auth
@csrf_exempt
def can_see(request, author_id, post_id):
    author = Author.objects.get(id=author_id)
    post = Post.objects.get(id=post_id)

    if author_can_see_post(author, post):
        return JsonResponse({"cansee": True})
    else:
        return JsonResponse({"cansee": False})
