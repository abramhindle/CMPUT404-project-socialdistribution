from django.conf import settings
from django.contrib.auth import (authenticate,
                                 login as auth_login, logout as auth_logout)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
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
                # We need to make sure we aren't logging in with a remote
                # author...
                if author[0].host == settings.LOCAL_HOST:
                    auth_login(request, user)
                    return HttpResponseRedirect('/author/posts/', status=302)
                else:
                    context['error'] = ('The username and/or password is '
                                        'incorrect.')
            else:
                # An error occurred
                context['error'] = 'The username and/or password is incorrect.'

        return render_to_response('login.html', context)
    else:
        return HttpResponseRedirect('/author/posts/', status=302)


@login_required
def logout(request):
    if request.user.is_authenticated():
        """Logs the current logged in user out of the web application."""
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


def profile_self(request):
    """Redirect to the logged in Author's profile"""
    context = RequestContext(request)

    if request.user.is_authenticated():

        if request.method == 'GET':
            try:
                author = Author.objects.get(user=request.user)
                return redirect('/author/%s' % author.uuid)

            except Author.DoesNotExist:
                return _render_error('login.html', 'Please log in.', context)
        else:
            return _render_error('login.html', 'Invalid request.', context)
    else:
        return _render_error('login.html', 'Please log in.', context)


def profile(request, author_id):
    """Display the author's profile and profile updates if authenticated."""
    context = RequestContext(request)

    if request.user.is_authenticated():

        if request.method == 'GET':
            # Display the profile page
            try:
                author = Author.objects.get(uuid=author_id)

                context['username'] = author.user
                context['github_username'] = author.github_user
                context['host'] = author.host

                if author_id != Author.objects.get(user=request.user).uuid:
                    context['readonly'] = True
                else:
                    context['readonly'] = False

                return render_to_response('profile.html', context)
            except Author.DoesNotExist:
                return _render_error('login.html', 'Please log in.', context)

        elif request.method == 'POST':
            # Update the profile information
            github_user = request.POST['github_username']
            password = request.POST['password']

            author = Author.objects.get(user=request.user)
            if author.uuid == author_id:
                # Make sure we have the permissions
                author.github_user = github_user

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
                    context['host'] = author.host
                    return render_to_response('profile.html', context)

            else:
                return _render_error('login.html', 'Invalid request.', context)
        else:
            return _render_error('login.html', 'Invalid request.', context)

    else:
        return _render_error('login.html', 'Please log in.', context)

def post_redirect(request, author_id):
    context = RequestContext(request)



def register(request):
    """Register creates a new Author in the system.

    If the information is invalid, the error information will be displayed.
    """
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['userName']
        password = request.POST['pwd']
        github_user = request.POST['github_username']

        # check if its a unique username
        if len(User.objects.filter(username=username)) > 0:
            context = RequestContext(
                request,
                {
                    'userNameValidity':
                    'The username "%s" is taken' % username,
                    'github_username': "%s" % github_user
                })
        #check if there are spaces in username
        elif " " in username:
            context = RequestContext(
                request,
                {
                    'userNameValidity':
                    'The username "%s" cannot contain spaces' % username,
                    'github_username': "%s" % github_user
                })
        else:
            if username and password:
                user = User.objects.create_user(username=username,
                                                password=password)

                author = Author.objects.create(user=user,
                                               github_user=github_user)
                return redirect('/')

    return render_to_response('register.html', context)


def search(request):
    """Returns a list of authors.

    The returned list of authors contains their username, first_name,
    and last_name.
    """
    context = RequestContext(request)

    if request.method == 'POST':
        searchValue = request.POST['searchValue']

        if searchValue == "":
            return redirect('/')

        AuthoInfo = []

        #query all values containing search results
        users = User.objects.filter(Q(username__contains=searchValue) &
                                    ~Q(username=request.user))

        results = 0
        status = None
        #setting each author search information
        for user in users:
            friend = False
            sent = False
            received = False
            results += 1
            status = FriendRequest.get_status(request.user, user)
            if status is not None:
                if status:
                    friend = True
                else:
                    sent = True
            else:
                status = FriendRequest.get_status(user, request.user)
                if status is not None:
                    if status:
                        friend = True
                    else:
                        received = True
            author = Author.objects.get(user=user)
            #check if user is a remote user
            #local host should not have spaces in their username
            try:
                username = user.username.split(" ")[0]
            except:
                username = user.id

            userInfo = {"displayname": username,
                        "userID": author.uuid,
                        "host": author.host,
                        "friend": friend,
                        "sent": sent,
                        "received": received}

            AuthoInfo.append(userInfo)

        context = RequestContext(request, {'searchValue': searchValue,
                                           'authorInfo': AuthoInfo,
                                           'status': status,
                                           'results': results})
    return render_to_response('searchResults.html', context)


def request_friendship(request):
    """Sends a friend request."""
    context = RequestContext(request)

    if request.method == 'POST':
        if request.user.is_authenticated():
            friendRequestee = request.POST['friend_requestee']
            friendUser = User.objects.get(username=friendRequestee)
            friend = Author.objects.get(user=friendUser)
            requester = Author.objects.get(user=request.user)
            status = FriendRequest.make_request(requester, friend)

            if status:
                messages.info(request, 'Friend request sent successfully')
            else:
                messages.error(request, 'Error sending a friend request')

            return redirect('/')
        else:
            _render_error('login.html', 'Please log in.', context)


def accept_friendship(request):
    """Handles a post request to accept a friend request."""
    context = RequestContext(request)

    if request.method == 'POST':
        if request.user.is_authenticated():
            friendRequester = request.POST['friend_requester']
            requester = User.objects.get(username=friendRequester)
            requester2 = Author.objects.get(user=requester)
            author = Author.objects.get(user=request.user)
            status = FriendRequest.accept_request(author, requester2)

            if status:
                messages.info(request, 'Friend request has been accepted.')
            return redirect('/', context)
        else:
            _render_error('login.html', 'Please log in.', context)

def reject_friendship(request):
    """Handles a request to reject a friend request."""
    context = RequestContext(request)
    print("here")
    if request.method == 'POST':
        print("in post")
        if request.user.is_authenticated():
            friendRequester = request.POST['friend_requester']
            requester = User.objects.get(username=friendRequester)
            requester2 = Author.objects.get(user=requester)
            author = Author.objects.get(user=request.user)
            print(author)
            status = FriendRequest.reject_request(author, requester2)

            if status:
                messages.info(request, 'Friend request has been rejected.')
            return redirect('/', context)
        else:
            _render_error('login.html', 'Please log in.', context)



def friend_request_list(request, author):
    """Displays a list of users that the author sent a friend requst to."""
    context = RequestContext(request)

    if request.method == 'GET':
        if request.user.is_authenticated():
            requestList = []
            sentList = []
            for author in FriendRequest.received_requests(request.user):
                requestList.append(author.user.username)
            for author in FriendRequest.sent_requests(request.user):
                sentList.append(author.user.username)
            context = RequestContext(request, {'requestList' : requestList,
                                                'sentList' : sentList})
        else:
            _render_error('login.html', 'Please log in.', context)

    return render_to_response('friendRequests.html', context)

def friend_list(request, author):
    """Gets the user's friends."""
    context = RequestContext(request)

    if request.method == 'GET':
        if request.user.is_authenticated():
            friendUsernames = []
            author = Author.objects.get(user=request.user)
            friendList = FriendRequest.get_friends(author)

            for friend in friendList:
                friendUsernames.append(friend.user)

            context = RequestContext(request, {'friendList': friendUsernames})
        else:
            _render_error('login.html', 'Please log in.', context)
    return render_to_response('friends.html', context)


def _render_error(url, error, context):
    context['error'] = error
    return render_to_response(url, context)
