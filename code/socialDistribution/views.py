from django.http.response import *
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout, get_user_model

from .forms import CreateUserForm
from .decorators import allowedUsers, unauthenticated_user
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.shortcuts import redirect
from django.db.models import Count
from .models import *
from datetime import datetime

REQUIRE_SIGNUP_APPROVAL = False
''' 
    sign up approval not required by default, should turn on in prod. 
    if time permits store this in database and allow change from admin dashboard.
'''

def get_home_context(author, error, msg=''):
    context = {}
    context['author'] = author
    context['modal_type'] = 'post'
    latest_posts = Post.objects.filter(unlisted=False).order_by("-pub_date")[:5]
    context['latest_posts'] = latest_posts
    context['error'] = error
    context['error_msg'] = msg
    return context

def index(request):
    """
        Redirect User on visiting /
    """
    if request.user.is_authenticated:
        author_id = get_object_or_404(Author, user=request.user).id
        return redirect('socialDistribution:home', author_id=author_id)
    else:
        return redirect('socialDistribution:login')

        
@unauthenticated_user
def loginPage(request):
    """
        Logs in a user and redirects to Home page
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        User = get_user_model()

        # check if user is active
        try: 
            user = User.objects.get(username=username)
        except Exception:
            messages.info(request, "Login Failed. Please try again.")
            return render(request, 'user/login.html')

        if REQUIRE_SIGNUP_APPROVAL and not user.is_active:
            # user inactive
            messages.info(request, "Your account is currently pending approval. Please check back later.")
        else:
            # user active, proceed to authentication
            user = authenticate(request, username=username, password=password)

            try:
                author_id = Author.objects.get(user=user).id

                if user is not None:
                    login(request, user)
                    return redirect('socialDistribution:home', author_id=author_id)
                else:
                    raise KeyError

            except (KeyError, Author.DoesNotExist):
                messages.info(request, "Username or Password is incorrect.")

    return render(request, 'user/login.html')

@unauthenticated_user
def register(request):
    """
        Registers a new user and redirects to Login page
    """
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            try:
                # extract form data
                username = form.cleaned_data.get('username')
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                github_url = request.POST.get('github_url', '')
                full_name = f"{first_name} {last_name}"

                # check github url
                if (github_url and not github_url.startswith('https://github.com/')):
                    context = { 'form': form }
                    form.errors['github_url'] = 'Invalid github url, must be of format: https://github.com/username'
                    return render(request, 'user/register.html', context)

                user = form.save()

                if REQUIRE_SIGNUP_APPROVAL:
                    # admin must approve user from console 
                    user.is_active = False 

                user.save()

                # add user to author group by default
                group, created = Group.objects.get_or_create(name="author")
                user.groups.add(group)
                author = Author.objects.create(
                    user=user,
                    username=username,
                    displayName=full_name,
                    githubUrl=github_url
                )
                Inbox.objects.create(author=author)
            except:
                return HttpResponse("Sign up failed. Internal Server Error. Please Try again.", status=500)
            
            if REQUIRE_SIGNUP_APPROVAL:
                messages.success(request, f'Account creation request sent to admin for {username}.')
            else:
                messages.success(request, f'Account created for {username}.')

            # On successful sign up request, redirect to login page
            return redirect('socialDistribution:login')
        
    context = { 'form': form }
    return render(request, 'user/register.html', context)

def logoutUser(request): 
    """
        Logoust out a user and redirects to login page
    """
    logout(request)
    return redirect('socialDistribution:login')

def home(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    context = get_home_context(author, False)
    return render(request, 'home/index.html', context)

def accept_friend(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    curr_user = Author.objects.get(user=request.user)

    if curr_user.id != author.id and curr_user.inbox.has_req_from(author) \
        and not curr_user.has_follower(author):
        curr_user.inbox.follow_requests.remove(author)
        curr_user.followers.add(author)
    else:
        messages.info(request, f'Couldn\'t accept request')

    return redirect('socialDistribution:author', author_id)

def befriend(request, author_id):
    if request.method == 'POST':
        author = get_object_or_404(Author, pk=author_id)
        curr_user = Author.objects.get(user=request.user)

        if author.has_follower(curr_user):
            messages.info(request, f'Already following {author.displayName}')

        if author.inbox.has_req_from(curr_user):
            messages.info(request, f'Follow request to {author.displayName} is pending')

        if author.id != curr_user.id:
            # send follow request
            author.inbox.follow_requests.add(curr_user)

    return redirect('socialDistribution:author', author_id)

def un_befriend(request, author_id):
    if request.method == 'POST':
        author = get_object_or_404(Author, pk=author_id)
        curr_user = Author.objects.get(user=request.user)
        
        if author.has_follower(curr_user):
            author.followers.remove(curr_user)
        else:
            messages.info(f'Couldn\'t un-befriend {author.displayName}')

    return redirect('socialDistribution:author', author_id)

#@allowedUsers(allowed_roles=['author']) # just for demonstration
def authors(request):
    args = {}

    # demonstration purposes: Authors on remote server
    remote_authors = [
        {
            "data": {
                "id": 16000,
                "username": "johnd",
                "displayName": "John Doe",
                "post__count": 0,
            },
            "type": "Remote"
        },
        {
            "data": {
                "id": 15000,
                "username": "janed",
                "displayName": "Hane Doe",
                "post__count": 0
            },
            "type": "Remote"
        }
    ]

    # Django Software Foundation, "Generating aggregates for each item in a QuerySet", 2021-10-13
    # https://docs.djangoproject.com/en/3.2/topics/db/aggregation/#generating-aggregates-for-each-item-in-a-queryset
    authors = Author.objects.all().annotate(Count("post"))
    local_authors = [{
            "data": author,
            "type": "Local"
        } for author in authors]

    args["authors"] = local_authors + remote_authors
    return render(request, 'author/index.html', args)

def author(request, author_id):
    curr_user = Author.objects.get(user=request.user)
    author = get_object_or_404(Author, pk=author_id)
    posts = Post.objects.filter(author__pk=author.id)
    context = {
        'author': author,
        'author_type': 'Local',
        'curr_user': curr_user,
        'author_posts': posts
    }

    return render(request, 'author/detail.html', context)

def create(request):
    return render(request, 'create/index.html')

def posts(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        source = request.POST.get('source')
        origin = request.POST.get('origin')
        categories = request.POST.get('categories').split()
        img = request.POST.get('img')
        description = request.POST.get('description')
        content = request.POST.get('content')
        visibility = request.POST.get('visibility')
        is_unlisted = request.POST.get('unlisted')
        pub_date = datetime.now()

        if is_unlisted is None:
            is_unlisted = False
        else:
            is_unlisted = True

        if visibility == '1':
            visibility = Post.PostVisibility.FRIENDS
        else:
            visibility = Post.PostVisibility.PUBLIC
        
        # temporarily set to zero; will need to fix that soon!
        page_size = 0
        count = 0

        try:
            post = Post.objects.create(
                author_id=author_id,  # temporary
                title=title, 
                source=source, 
                description=description,
                content_text=content,
                visibility=visibility,
                pub_date=pub_date,
                unlisted=is_unlisted,
                page_size=page_size,
                count=count
            )

            for category in categories:
                Category.objects.create(category=category, post=post)

        except ValidationError:
            context = get_home_context(author, True, "Something went wrong! Couldn't create post.")
            return render(request, 'home/index.html', context)

        else:
            # if using view name, app_name: must prefix the view name
            # In this case, app_name is socialDistribution
            return redirect('socialDistribution:home', author_id=author_id)
    
    return render(request, 'posts/index.html')

# https://www.youtube.com/watch?v=VoWw1Y5qqt8 - Abhishek Verma
def likePost(request, id):
    # move functionality to API
    post = get_object_or_404(Post, id = id)
    author = Author.objects.get(user=request.user)
    if post.likes.filter(id=author.id).exists():
        post.likes.remove(author)
    else:
        post.likes.add(author)
    return redirect('socialDistribution:home', author_id=author.id)

def commentPost(request, id):
    '''
        Render Post and comments
    '''
    post = get_object_or_404(Post, id = id)
    author = get_object_or_404(Author, user=request.user)

    try:
        comments = Comment.objects.filter(post=post).order_by('-pub_date')
    except Exception:
        return HttpResponseServerError()

    context = {
        'author': author,
        'author_type': 'Local',
        'modal_type': 'post',
        'post': post,
        'comments': comments
    }
    
    return render(request, 'posts/comments.html', context)



def deletePost(request, id):
    # move functionality to API
    post = get_object_or_404(Post, id = id)
    author = Author.objects.get(user=request.user)
    if post.author == author:
        post.delete()
    return redirect('socialDistribution:home', author_id=author.id)

def editPost(request, id):
    # todo
    return render(request, 'create/index.html')

def profile(request):
    return render(request, 'profile/index.html')

def user(request):
    return render(request, 'user/index.html')
