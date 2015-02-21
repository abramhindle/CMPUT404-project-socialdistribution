from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext

from author.models import Author


def login(request):
    """Validate the user, password combination on login.

    If successful, redirect the user to the home page, otherwise, return an
    error in the response.
    """
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's built in authentication to verify if the username and
        # password combination is valid
        user = authenticate(username=username, password=password)
        author = Author.objects.filter(user=user)
        if len(author) > 0:
            login(request, user)
            return redirect('to-add.html')
        else:
            # An error occurred
            context['message'] = 'The username and/or password is incorrect.'

    return render_to_response('login.html', context)
