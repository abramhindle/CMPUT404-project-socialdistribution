from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render


def root(request: HttpRequest) -> HttpResponse:
    if request.user.is_anonymous:
        return redirect(reverse_lazy('auth_provider:login'))
    return render(request, 'stream.html')
