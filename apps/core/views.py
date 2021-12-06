from django.http.request import HttpRequest
from django.http.response import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.urls.base import reverse
from django.views import generic
from .models import ExternalHost, User, Author, Follow
from .serializers import AuthorSerializer
from apps.posts.models import Post
from apps.posts.serializers import PostSerializer
from socialdistribution.utils import Utils
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.core.exceptions import MultipleObjectsReturned

# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'core/index.html'

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", )

class SignUpView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse('login')

def followers(request: HttpRequest):
    if request.user.is_anonymous:
        return render(request,'core/index.html')

    currentAuthor = Author.objects.filter(userId=request.user).first()
    return followers_with_target(request, currentAuthor.id)

def followers_with_target(request: HttpRequest, author_id: str):
    currentAuthor = Author.objects.filter(userId=request.user).first()
    if request.user.is_anonymous or (currentAuthor.id != author_id and not request.user.is_staff):
        return render(request,'core/index.html')

    host = Utils.getRequestHost(request)
    target_host = Utils.getUrlHost(author_id)
    followers = []
    followerUrl = author_id +"/followers"
    if (not target_host):
        follows = Follow.objects.filter(target=author_id)
        for follow in follows:
            followers.append(follow.follower)
        serializer = AuthorSerializer(followers, context={'host': host}, many=True)
        followers = serializer.data
    else:
        followers = Utils.getFromUrl(followerUrl)
        followers = followers["data"] if followers and followers.__contains__("data") else []
    
    target_author: dict = Utils.getAuthorDict(author_id, host)
    if (not target_author):
        return HttpResponseNotFound

    # Add foreign nodes
    hosts = list(ExternalHost.objects.values_list('host', flat=True))
    host_in_list = False
    for i, h in enumerate(hosts):
        if (Utils.areSameHost(h, host)):
            hosts[i] = host
            host_in_list = True
    
    if (not host_in_list):
        hosts.append(host)

    context = {
        'title': "My Followers",
        'is_staff': request.user.is_staff,
        'author' : currentAuthor, 
        'authors': followers, 
        'host': host,
        'hosts': hosts,
        'selected_host': target_host if target_host else host,
    }
    return render(request, 'authors/index.html', context)

def authors(request: HttpRequest):
    if request.user.is_anonymous:
        return render(request,'core/index.html')
    currentAuthor=Author.objects.filter(userId=request.user).first()

    target_host = request.GET.get('target_host', None)
    host = Utils.getRequestHost(request)
    authors = None
    if (not target_host or target_host == host):
        if (request.user.is_staff):
            authors = Author.objects.all()
        else:
            authors = Author.objects.filter(isApproved=True)
        serializer = AuthorSerializer(authors, context={'host': host}, many=True)
        authors = serializer.data
    else:
        authorUrl = target_host + "/authors"
        response = Utils.getFromUrl(authorUrl)
        if (response and response["data"]):
            authors = response["data"]
        else:
            return HttpResponseNotFound

    hosts = list(ExternalHost.objects.values_list('host', flat=True))
    host_in_list = False
    for i, h in enumerate(hosts):
        if (Utils.areSameHost(h, host)):
            hosts[i] = host
            host_in_list = True
    
    if (not host_in_list):
        hosts.append(host)

    context = {
        'title': "Authors",
        'is_staff': request.user.is_staff,
        'author' : currentAuthor, 
        'authors': authors, 
        'host': host,
        'hosts': hosts,
        'selected_host': target_host if target_host else host,
    }
    return render(request, 'authors/index.html', context)

def author(request: HttpRequest, author_id: str):
    host = Utils.getRequestHost(request)
    currentAuthor=Author.objects.filter(userId=request.user).first()

    if request.user.is_anonymous:
        return render(request,'core/index.html')
    
    is_following = False
    is_follower = False

    target_id = Utils.cleanAuthorId(author_id, host)
    follower_id = Utils.cleanAuthorId(currentAuthor.id, host)
    if (target_id != follower_id):
        try:
            follow = Follow.objects.get(follower_id=follower_id, target_id=target_id)
            if (follow):
                is_following = True
        except:
            is_following = False

        try:
            follow = Follow.objects.get(follower_id=target_id, target_id=follower_id)
            if (follow):
                is_follower = True
        except:
            is_follower = False

    target_host = Utils.getUrlHost(target_id)
    if (not target_host or Utils.areSameHost(target_host, host)):
        target_host = host

    if target_host == host:
        author_uuid = Utils.getAuthorId(author_id)
        if (author_uuid is None):
            author_uuid = author_id
        authorPosts = get_object_or_404(Author, id=author_uuid)
        posts = PostSerializer(Post.objects.filter(author=authorPosts), context={'host': host}, many=True).data
    else:
        posts = Utils.getFromUrl(target_id+"/posts")
        if (posts.__contains__("data")):
            posts = posts["data"]


    serializer = AuthorSerializer(currentAuthor, context={'host': host})
    currentAuthor = serializer.data
    context = {
        'host':host,
        'author' : currentAuthor, 
        'author_id' : currentAuthor["url"], 
        'is_staff': request.user.is_staff,
        'target_author_id' : author_id,
        'target_host' : target_host,
        'is_following': is_following,
        'is_follower': is_follower,
        'can_edit': target_host == host and (request.user.is_staff or target_id == follower_id),
        'posts': posts
    }
    return render(request,'authors/author.html',context)

def friend_requests(request: HttpRequest):
    # Drop if not logged in
    if request.user.is_anonymous:
        return render(request,'core/index.html')

    currentAuthor=Author.objects.filter(userId=request.user).first()

    target_host = request.GET.get('target_host', None)
    host = Utils.getRequestHost(request)

    followers = []
    if (not target_host or target_host == host):
        # Get followers
        followersQuerySet = Follow.objects.filter(target=currentAuthor.id)
        for follower in followersQuerySet:
            # Check we are not following this follower
            try:
                follow = Follow.objects.get(follower=currentAuthor.id, target=follower.follower.id)
            except Follow.DoesNotExist:
                follow = None
            except MultipleObjectsReturned:
                # We should ideally fix a bug when user can follow itself multiple times
                follow = Follow.objects.filter(follower=currentAuthor.id, target=follower.follower.id)[0]

            if (not follow):
                followers.append(follower.follower)
        serializer = AuthorSerializer(followers, context={'host': host}, many=True)
        followers = serializer.data
    # Not fully implemented
    # else:
    #     followersUrl = host + "/author/" + currentAuthor.id + "/followers"
    #     response = Utils.getFromUrl(followersUrl)
    #     if (response and response["data"]):
    #         followersList = response["data"]
    #         for follower in followersList:
    #             checkFollower = followersUrl + "/" + follower.id
    #             if checkFollower:
    #                 followers += follower
            
    #     else:
    #         return HttpResponseNotFound

    # Add foreign nodes
    hosts = list(ExternalHost.objects.values_list('host', flat=True))
    host_in_list = False
    for i, h in enumerate(hosts):
        if (Utils.areSameHost(h, host)):
            hosts[i] = host
            host_in_list = True
    
    if (not host_in_list):
        hosts.append(host)

    context = {
        'title': "Friend Requests",
        'is_staff': request.user.is_staff,
        'author' : currentAuthor, 
        'authors': followers, 
        'host': host,
        'hosts': hosts,
        'selected_host': target_host if target_host else host,
    }
    return render(request, 'authors/index.html', context)

# def author(request: HttpRequest):
#     host = Utils.getRequestHost(request)
#     author_id = request.GET.get('author_id', None)
#     if (not author_id):
#         return redirect(reverse('core:authors'))

#     author_id = Utils.cleanAuthorId(author_id, host)
#     currentAuthor=Author.objects.filter(userId=request.user).first()
#     if request.user.is_anonymous or (currentAuthor.id != author_id and not request.user.is_staff):
#         return render(request,'core/index.html')
    
#     target_author: dict = Utils.getAuthorDict(author_id, host)
#     if (not target_author):
#         return HttpResponseNotFound

#     is_following = False
#     try:
#         follow = Follow.objects.get(follower_id=currentAuthor.id, target_id = author_id)
#         if (follow):
#             is_following = True
#     except:
#         is_following = False

#     host = request.scheme + "://" + request.get_host()
#     context = {
#         'host':host,
#         'author': AuthorSerializer(currentAuthor, context={'host': host}).data,
#         'is_staff': request.user.is_staff,
#         'target_author' : target_author,
#         'is_following': is_following
#     }
#     return render(request,'authors/author.html',context)