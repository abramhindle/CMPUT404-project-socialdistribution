from django.contrib import auth
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext


def login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        #user = authenticate(username=username, password=password)

    return render_to_response('login.html', context)
