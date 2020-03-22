import base64

from django.http import HttpResponse
from django.contrib.auth import authenticate, login

#############################################################################
#

def check_view(view):
    def view_or_basicauth(request, *args, **kwargs):
        """
        Check first is user is logged in and authenticated
        """
        if request.user.is_authenticated:
            # Already logged in, just return the view.
            return view(request, *args, **kwargs)

        # They are not logged in. See if they provided HTTP BASIC AUTH credentials
        if 'HTTP_AUTHORIZATION' in request.META:
            print(request.META['HTTP_AUTHORIZATION'])
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if auth[0].lower() == "basic":
                uname, passwd = base64.b64decode(auth[1]).decode('utf-8').split(':', 1)

                #Check if user exists
                user = authenticate(username=uname, password=passwd)

                #If user exists, and is active, login user and then check that they're authenticated, then return view
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        request.user = user
                        if request.user.is_authenticated:
                            return view(request, *args, **kwargs)

        print(request.headers)

        # If request does not have active user, or not HTTP Basic Auth, return 403.
        response = HttpResponse()
        response.status_code = 403

        return response

    return view_or_basicauth

#############################################################################
#
def logged_in_or_basicauth():
    """
    A simple decorator that requires a user to be logged in. If they are not
    logged in the request is examined for a 'authorization' header.
    If the header is present it is tested for basic authentication and
    the user is logged in with the provided credentials.
    If the header is not present a http 401 is sent back to the
    requestor to provide credentials.
    The purpose of this is that in several django projects I have needed
    several specific views that need to support basic authentication, yet the
    web site as a whole used django's provided authentication.
    The uses for this are for urls that are access programmatically such as
    by rss feed readers, yet the view requires a user to be logged in. Many rss
    readers support supplying the authentication credentials via http basic
    auth (and they do NOT support a redirect to a form where they post a
    username/password.)
    Use is simple:
    @logged_in_or_basicauth()
    def your_view:
        ...
    You can provide the name of the realm to ask for authentication within.
    """
    def view_decorator(func):
        def wrapper(request, *args, **kwargs):
            return view_or_basicauth( request,
                                     lambda u: u.is_authenticated(),
                                      *args, **kwargs)
        return wrapper
    return view_decorator
