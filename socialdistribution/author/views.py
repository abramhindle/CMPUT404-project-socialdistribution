from django.contrib.auth import (authenticate,
                                 login as auth_login, logout as auth_logout)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.cache import cache
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext

from author.models import Author, FriendRequest
from django.contrib import messages


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
                return HttpResponseRedirect('/author/posts/', status=302)
            else:
                # An error occurred
                context['error'] = 'The username and/or password is incorrect.'

        return render_to_response('login.html', context)
    else:
        return HttpResponseRedirect('/author/posts/', status=302)


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
        return _render_error('login.html', 'Invalid request.', context)


def profile(request, author):
    """Display the author's profile and handle profile updates."""
    context = RequestContext(request)

    if request.user.is_authenticated():

        if request.method == 'GET':
            # Display the profile page
            try:
                author = Author.objects.get(user=request.user)

                context['github_username'] = author.github_user
                context['first_name'] = author.user.first_name
                context['last_name'] = author.user.last_name
                return render_to_response('profile.html', context)
            except Author.DoesNotExist:
                return _render_error('login.html', 'Please log in.', context)

        elif request.method == 'POST':

            # Update the profile information
            github_user = request.POST['github_username']
            password = request.POST['password']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']

            author = Author.objects.get(user=request.user)
            author.github_user = github_user
            author.user.first_name = first_name
            author.user.last_name = last_name

            if len(password) > 0:
                # Password is changed, we need to force a re-login.
                author.user.set_password(password)
                author.user.save()
                author.save()
                return redirect('/')
            else:
                author.user.save()
                author.save()
                context['success'] = 'Successfully updated!'
                context['github_username'] = author.github_user
                context['first_name'] = author.user.first_name
                context['last_name'] = author.user.last_name
                return render_to_response('profile.html', context)

        else:
            return _render_error('login.html', 'Invalid request.', context)

    else:
        return _render_error('login.html', 'Please log in.', context)


def register(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['userName']
        password = request.POST['pwd']
        first_name = request.POST['fName']
        last_name = request.POST['lName']
        github_user = request.POST['github_username']

        # check if its a unique username
        if len(User.objects.filter(username=username)) > 0:
            context = RequestContext(
                request,
                {
                    'userNameValidity':
                    'The username %s is already being used' % username,
                    'fNameSaved': "%s" % first_name,
                    'lNameSaved': "%s" % last_name
                })
        else:
            if username and password:
                user = User.objects.create_user(username=username,
                                                password=password,
                                                first_name=first_name,
                                                last_name=last_name)

                author = Author.objects.create(user=user,
                                               github_user=github_user)
                return redirect('/')

    return render_to_response('register.html', context)


def search(request):
    """
    Returns a list of authors containing their username, first_name, and last_name
    """
    context = RequestContext(request)

    if request.method == 'POST':
        searchValue = request.POST['searchValue']

        if searchValue == "":
            return redirect('/')

        AuthoInfo = []

        #query all values containing search results
        users = User.objects.filter(
                    Q(username__contains=searchValue) & ~Q(username=request.user))

        results=0

        #setting each author search information
        for user in users:
            results +=1
            userInfo = {"displayname": user.username,
                          "userID":user.id,
                          "first_name": "name: " +user.first_name,
                          "last_name":user.last_name}

            AuthoInfo.append(userInfo)

        context = RequestContext(request, {'searchValue': searchValue,
                                           'authorInfo': AuthoInfo,
                                           'results':results})
    return render_to_response('searchResults.html', context)

def request_friendship(request) :
    """
    Sends a friend request
    """
    context = RequestContext(request)

    if request.method == 'POST':
        friendRequestee = request.POST['friend_requestee']
        print(friendRequestee)
        """friendRequestee = request.POST['friend_requester']"""
        #friend = Author.objects.select_related('requestee').get(pk = friendRequestee)
        friend = User.objects.get(username=friendRequestee)
        requester = User.objects.get(username = request.user)
        newEntry = FriendRequest(requestee = friend, requester = requester)
        newEntry.save()

        messages.info(request, 'Friend request sent successfully')
        return render_to_response('searchResults.html', context)

def friend_request_list(request, author) :
    """
    Gets the list of users that sent the author a friend request and displays them in the html
    """
    context = RequestContext(request)
    if request.method == 'POST' :
        requestList = []
        results = FriendRequest.pending_requests(request.user)
        for userObject in results:                 # for each FriendRequest object (contains both the author and requester)
            requestList.append(userObject.requester)
            print(userObject.requester)       # Get just the requester and then the user derived from the Author object
        context = RequestContext(request, {'requestList' : requestList})
    return render_to_response('friendRequests.html', context)

def _render_error(url, error, context):
    context['error'] = error
    return render_to_response(url, context)

