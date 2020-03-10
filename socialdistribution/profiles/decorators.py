from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic.base import RedirectView

def check_authentication(view_to_check):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_to_check(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/403/')
    return wrapper_func