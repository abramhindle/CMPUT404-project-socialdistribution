from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from requests.auth import HTTPBasicAuth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    else:
        return HttpResponseRedirect(reverse('login'))


@login_required(login_url='/login')
def home(request):
    if request.method == "POST":
        request_data = request.data.copy()
    return render(request, "home.html")


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            ...
            return HttpResponseRedirect(reverse('login'))


def login(request):
    pass


def profile(request):
    pass
