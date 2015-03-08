from datetime import datetime
from django.core.cache import cache
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpRequest
from django.template import RequestContext
from post.models import Post, AuthoredPost, VisibleToAuthor
from author.models import Author

import requests
import json


def createPost(request):
    context = RequestContext(request)

    if request.method == "POST":
        if request.user.is_authenticated():
            text = request.POST.get("text_body", "")
            author = Author.objects.get(user=request.user)
            visibility = request.POST.get("visibility_type", "")
            # TODO: not sure whether to determine type or have user input type
            mime_type = "text/plain"

            new_post = Post.objects.create(text=text,
                                           mime_type=mime_type,
                                           visibility=visibility)

            AuthoredPost.objects.create(author=author, post=new_post)

            #TODO: should prob not do this
            if visibility == Post.ANOTHER_AUTHOR:
                try:
                    #TODO somehow change this to get the actual author
                    visible_author = request.POST.get("visible_author", "")
                    visible_author_obj = Author.objects.get(
                        user=visible_author)

                    VisibleToAuthor.objects.create(
                        visibleAuthor=visible_author_obj, post=new_post)
                except Author.DoesNotExist:
                    #TODO: not too sure if care about this enough to handle it
                    print("hmm")
        else:
            return redirect('login.html', 'Please log in.', context)

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
                posts = list(posts) + _get_github_events(author)

                # Sort posts by date
                posts.sort(key=lambda
                           item: item.post.publication_date,
                           reverse=True)

                visibility_types = post_instance.getVisibilityTypes()
                return render_to_response(
                    'index.html',
                    {'posts': posts, 'visibility': visibility_types}, context)
            except Author.DoesNotExist:
                return _render_error('login.html', 'Please log in.', context)
        else:
            return _render_error('login.html', 'Please log in.', context)
    else:
        return _render_error('login.html', 'Invalid request.', context)


# def posts(request):

# def post(request, post_id):

def _get_github_events(author):
    headers = {'Connection': 'close'}

    if len(author.github_etag) > 0:
        headers['If-None-Match'] = author.github_etag

    url = 'https://api.github.com/users/%s/events' % author.github_user

    response = requests.get(url, headers=headers)

    print response

    # We didn't get a response or we've reached our GitHub limit of 60.
    if not response or int(response.headers["X-RateLimit-Remaining"]) == 0:
        return []

    if response.status_code == 200:
        # Store the etag for future use
        author.github_etag = response.headers['ETag']
        author.save()

        events = []

        for event in response.json():
            date = datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ')

            post = Post(text=event['payload'],
                        mime_type=Post.PLAIN_TEXT,
                        visibility=Post.PRIVATE,
                        publication_date=date)

            authored_post = AuthoredPost(post=post, author=author)

            events.append(authored_post)

        # Cache these results in the event that we've reached our rate
        # limit, or we get a 304 because the events haven't changed.
        cache.set(author.user.id, events, None)
        return events
    elif response.status_code == 304:
        # Results haven't changed, let's just return the cache, if one exists,
        # otherwise, we need to get it again.
        cached = cache.get(author.user.id)
        if cached is None:
            author.github_etag = ''
            return _get_github_events(author)
        else:
            return cached
    else:
        print 'ERROR: API at %s returned %d' % url, response.status_code
        return []


def _render_error(url, error, context):
    context['error'] = error
    return render_to_response(url, context)
