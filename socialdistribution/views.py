from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect


def root(request: HttpRequest) -> HttpResponse:
    if request.user.is_anonymous:
        return redirect('login')
    # TODO: redirect to user's stream page
    return HttpResponse("Main app")
