from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



from .forms import CreateUserForm

def index(request):
    return HttpResponse("Hello, world. You're at the Login/SignUp Page.")

def loginPage(request):
    """
        Logs in a user and redirects to Home page
    """
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))

    form = CreateUserForm()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        else:
            messages.info(request, "Username or Passoword is incorrect.")

    context = {}

    return render(request, 'user/login.html', context)
    
def register(request):
    """
        Registers a new user and redirects to Login page
    """
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

            user = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {user}')

            return HttpResponseRedirect(reverse('login'))

    context = { 'form': form }
    return render(request, 'user/register.html', context)

def logoutUser(request): 
    """
        Logoust out a user and redirects to login page
    """
    logout(request)
    return HttpResponseRedirect(reverse('login'))


@login_required(login_url="login")
def home(request):
    return render(request, 'home/index.html')

def authors(request):
    return render(request, 'authors/index.html')

def create(request):
    return render(request, 'create/index.html')

def post(request):
    return render(request, 'post/index.html')

def profile(request):
    return render(request, 'profile/index.html')

def user(request):
    return render(request, 'user/index.html')
