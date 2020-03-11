from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Author, AuthorFriend
from posts.forms import PostForm
from .forms import ProfileForm


def index(request):
    # This a view that display the navigation of the author. 
    # In the navigation, author can view/edit it's profile and dashboard.
    # Author can choose their actions such as look at the friends page,
    # post a new post, etc.
    # TODO: remove hardcode
    template = 'profiles/index_base.html'

    author = Author.objects.get(displayName='Xiaole')   #hardcode here

    context = {
        'author': author,
    }

    return render(request, template, context)

def new_post(request):

    # TODO: remove hardcode
    template = 'posts/posts_form.html'

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

    return render(request, template, context)

def current_visible_posts(request):
    return HttpResponse("Only these posts are visible to you: ")


def author_posts(request, author_id):
    return HttpResponse("Here are the posts of %s: ", author_id)

def view_profile(request):
    # TODO: remove hardcode
    template = 'profiles/profiles_view.html'

    author = Author.objects.get(displayName= 'Xiaole')

    context = {
        'author': author,
    }
    return render(request, template, context)


def edit_profile(request):
    # TODO: remove hardcode
    template = 'profiles/profiles_edit.html'

    author = Author.objects.get(displayName='Xiaole')   #hardcode here
    form = ProfileForm(request.POST or None, request.FILES or None, instance=author)

    context = {
        'form': form,
        'author': author,
    }

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            url = reverse('editprofile')
            return HttpResponseRedirect(url)

    return render(request, template, context)

def my_friends(request):
    # TODO: remove hardcode
    template = 'friends/friends_list.html'

    author = Author.objects.get(displayName='Xiaole')   #hardcode here
    friendList = AuthorFriend.objects.filter(author=author)

    context = {
        'author': author,
        'friendList': friendList,
    }
    return render(request, template, context)

def my_friend_requests(request):
    # TODO: remove hardcode
    template = 'friends/friends_request.html'

    author = Author.objects.get(displayName='Xiaole')   #hardcode here
    friendRequestList = AuthorFriend.objects.filter(friend=author)

    context = {
        'author': author,
        'friendRequestList': friendRequestList,
    }
    return render(request, template, context)

def my_friend_following(request):
    # TODO: remove hardcode
    template = 'friends/friends_follow.html'

    author = Author.objects.get(displayName='Xiaole')   #hardcode here
    friendFollowList = AuthorFriend.objects.filter(author=author)

    context = {
        'author': author,
        'friendFollowList': friendFollowList,
    }
    return render(request, template, context)

