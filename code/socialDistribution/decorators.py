from django.http import HttpResponse
from django.shortcuts import redirect

# ref: https://www.youtube.com/watch?v=eBsc65jTKvw&list=PL-51WBLyFTg2vW-_6XBoUpE7vpmoR3ztO&index=15 - Dennis Ivy
def unauthenticated_user(view_func):
    """
        Restrict to only if user is not authenticated
    """
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('socialDistribution:home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

def allowedUsers(allowed_roles=[]):
    """
        Authrorize user group
    """
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles or group == 'admin':
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authroized to view this page.')
        
        return wrapper_func
    return decorator
