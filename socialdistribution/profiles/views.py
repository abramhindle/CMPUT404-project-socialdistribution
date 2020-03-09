from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template.defaulttags import csrf_token

from .models import Author
from posts.forms import PostForm
from .forms import ProfileForm

# Create your views here.

def login(request):
    print("HELLO")
    return render(request, 'login.html', {'form': form})
    # return render(request, 'login/login.html', {})


def register(request):
    print("HELLO")
    if request.method == 'POST':
        print("IN HERE")
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('posts/')
    else:
        print("IN HERE")
        form = ProfileForm()
    return render(request, 'registration.html', {'form': form})

def index(request):
    author = Author.objects.get(displayName='Xiaole')   #hardcode here

    context = {
        'author': author,
    }

    return render(request, 'profiles/index_base.html', context)

def new_post(request):
    form = PostForm()
    author = Author.objects.get(displayName='Xiaole')


    context = {
        'form': form,
        'author': author,
    }

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            url = reverse('index')
            return HttpResponseRedirect(url)

    return render(request, 'posts/posts_form.html', context)

def current_visible_posts(request):
    return HttpResponse("Only these posts are visible to you: ")


def author_posts(request, author_id):
    return HttpResponse("Here are the posts of %s: ", author_id)

def view_profile(request):
    author = Author.objects.get(displayName= 'Xiaole')
    form = ProfileForm(instance=author)

    context = {
        'form': form,
        'author': author,
    }
    return render(request, 'profiles/profiles_view.html', context)


def edit_profile(request):
    author = Author.objects.get(displayName='Xiaole')   #hardcode here
    form = ProfileForm(request.POST or None, instance=author)

    context = {
        'form': form,
        'author': author,
    }

    if request.method == 'POST':

        if form.is_valid():
            form.save()
            url = reverse('editprofile')
            return HttpResponseRedirect(url)

    return render(request, 'profiles/profiles_edit.html', context)
