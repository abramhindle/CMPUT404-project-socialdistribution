from django.contrib.auth import (authenticate,
                                 login as auth_login, logout as auth_logout)
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext

from author.models import Author

import requests


def login(request):
    """Validate the user, password combination on login.

    If successful, redirect the user to the home page, otherwise, return an
    error in the response.
    """
    if not request.user.is_authenticated():
        context = RequestContext(request)

        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            # Use Django's built in authentication to verify if the username
            # and password combination is valid
            user = authenticate(username=username, password=password)
            author = Author.objects.filter(user=user)
            if len(author) > 0:
                auth_login(request, user)
                return redirect('/author/posts')
            else:
                # An error occurred
                context['error'] = 'The username and/or password is incorrect.'

        return render_to_response('login.html', context)
    else:
        return redirect('/author/posts')


@login_required
def logout(request):
    context = RequestContext(request)
    auth_logout(request)
    return redirect('/')


def home(request):
    """Display the author's home page."""
    context = RequestContext(request)

    if request.method == 'GET':
        if request.user.is_authenticated():
            try:
                author = Author.objects.get(user=request.user)
                return render_to_response('home.html', context)
            except Author.DoesNotExist:
                return _render_error('login.html', 'Please log in.', context)
        else:
            return _render_error('login.html', 'Please log in.', context)
    else:
        _render_error('login.html', 'Invalid request.', context)


def profile(request, author):
    """Display the author's profile and handle profile updates."""
    context = RequestContext(request)

    if request.user.is_authenticated():

        if request.method == 'GET':
            # Display the profile page
            try:
                author = Author.objects.get(user=request.user)

                context['github_username'] = author.github_user
                return render_to_response('profile.html', context)
            except Author.DoesNotExist:
                return _render_error('login.html', 'Please log in.', context)

        elif request.method == 'POST':

            # Update the profile information
            github_user = request.POST['github_username']
            password = request.POST['password']

            author = Author.objects.get(user=request.user)
            author.github_user = github_user

            if len(password) > 0:
                # Password is changed, we need to force a re-login.
                author.user.set_password(password)
                author.user.save()
                author.save()
                return redirect('/')
            else:
                author.save()
                context['success'] = 'Successfully updated!'
                context['github_username'] = author.github_user
                return render_to_response('profile.html', context)

        else:
            return _render_error('login.html', 'Invalid request.', context)

    else:
        _render_error('login.html', 'Please log in.', context)


def _render_error(url, error, context):
    context['error'] = error
    return render_to_response(url, context)


def _get_github_events(author):
    headers = {'Connection': 'close'}
    if len(author.github_etag) > 0:
        headers['If-None-Match'] = author.github_etag

    url = 'https://api.github.com/users/%s/events' % author.github_user

    response = requests.get(url, headers=headers, params={})

    # We didn't get a response or we've reached our GitHub limit of 60.
    if not response or int(response.headers["X-RateLimit-Remaining"]) == 0:
        return []

    if response.status_code == 200:
        # Store the etag for future use
        author.github_etag = response.headers['ETag']
        author.save()

        events = []

        # for event in response.json():

        # Cache these results in the event that we've reached our rate
        # limit, or we get a 304 because the events haven't changed.
        cache.set(author.user.id, events, None)
        return events
    elif response.status_code == 304:
        # Results haven't changed, let's just return the cache, if one exists
        return cache.get(author.user.id) or []
    else:
        print 'ERROR: API at %s returned %d' % url, response.status_code
        return []
