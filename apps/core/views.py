from django.core.paginator import Paginator
from django.http.request import HttpRequest
from django.http.response import HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.urls.base import reverse
from django.views import generic
from .models import ExternalHost, User, Author, Follow
from .serializers import AuthorSerializer
from apps.posts.models import Comment, Like, Post
from apps.posts.serializers import CommentSerializer, PostSerializer
from socialdistribution.utils import Utils
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import logout
from django.core.exceptions import MultipleObjectsReturned
from socialdistribution.pagination import DEFAULT_PAGE, DEFAULT_PAGE_SIZE

# Create your views here.
def IndexView(request: HttpRequest):
    if (request.user.is_authenticated and Utils.requiresApproval()):
        if (request.user.is_active):
            currentAuthor=Author.objects.filter(userId=request.user).first()
            if (not currentAuthor or not(currentAuthor.isServer or currentAuthor.isApproved or request.user.is_staff)):
                logout(request)
        else:
            logout(request)

    return Utils.defaultRender(request, 'core/index.html')

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
        return Utils.defaultRender(request,'core/index.html')

    currentAuthor = Author.objects.filter(userId=request.user).first()
    return followers_with_target(request, currentAuthor.id)

def followers_with_target(request: HttpRequest, author_id: str):
    currentAuthor = Author.objects.filter(userId=request.user).first()
    if request.user.is_anonymous or (currentAuthor.id != author_id and not request.user.is_staff):
        return Utils.defaultRender(request,'core/index.html')

    host = Utils.getRequestHost(request)
    target_host = Utils.getUrlHost(author_id)
    followers = []
    followerUrl = author_id +"/followers"
    if (not target_host):
        followerUrl = host + "/author/" + author_id + "/followers"
    followers = Utils.getFromUrl(followerUrl)
    followers = followers["data"] if followers and followers.__contains__("data") else []

    currentAuthor=Author.objects.filter(userId=request.user).first()
    if request.user.is_anonymous or (currentAuthor.id != author_id and not request.user.is_staff):
        return Utils.defaultRender(request,'core/index.html')

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
        'author' : currentAuthor, 
        'authors': followers, 
        'host': host,
        'hosts': hosts,
        'selected_host': target_host if target_host else host,
    }
    return Utils.defaultRender(request, 'authors/followers.html', context)

def authors(request: HttpRequest):
    if request.user.is_anonymous:
        return Utils.defaultRender(request,'core/index.html')
    currentAuthor=Author.objects.filter(userId=request.user).first()

    target_host = request.GET.get('target_host', None)
    host = Utils.getRequestHost(request)
    authors = None
    if (not target_host or target_host == host):
        if (request.user.is_staff):
            authors = Author.objects.all()
        else:
            if (Utils.requiresApproval()):
                authors = Author.objects.filter(isApproved=True, isServer=False)
            else:
                authors = Author.objects.filter(isServer=False)
        serializer = AuthorSerializer(authors, context={'host': host}, many=True)
        authors = serializer.data
    else:
        authorUrl = target_host + "/authors"
        response = Utils.getFromUrl(authorUrl)
        if (response and response.__contains__("data")):
            authors = response["data"]
        elif (response and response.__contains__("authors")):
            authors = response["authors"]
            for i, a in enumerate(authors):
                if a.__contains__("username") and (not a.__contains__("displayName") or not a["displayName"]):
                    authors[i]["displayName"] = a["username"]
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
        'author' : currentAuthor, 
        'authors': authors, 
        'host': host,
        'hosts': hosts,
        'selected_host': target_host if target_host else host,
    }
    return Utils.defaultRender(request, 'authors/index.html', context)

def author(request: HttpRequest, author_id: str):
    host = Utils.getRequestHost(request)
    currentAuthor=Author.objects.filter(userId=request.user).first()

    if request.user.is_anonymous:
        return Utils.defaultRender(request,'core/index.html')
    
    target_id = Utils.cleanAuthorId(author_id, host)
    target_author = Utils.getAuthorDict(target_id, host, True)

    is_following = False
    is_follower = False
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
        posts = Utils.getFromUrl(target_id+"/posts/")
        if (posts.__contains__("data")):
            posts = posts["data"]

    request_data = request.GET
    request_page = request_data.get("page", DEFAULT_PAGE)
    request_size = request_data.get("size", DEFAULT_PAGE_SIZE)

    paginator = Paginator(posts, request_size)
    try:
        posts_page = paginator.page(request_page)
    except:
        posts_page = []
    abs_path_no_query = request.build_absolute_uri(request.path)

    next_page = None
    if (posts_page != [] and posts_page.has_next()):
        next_page = posts_page.next_page_number()
    prev_page = None
    if (posts_page != [] and posts_page.has_previous()):
        prev_page = posts_page.previous_page_number()

    for post in posts_page:
        # fill comments inner stuff (likes)
        try:
            comments = get_3latest_comments(post["id"], target_host, host)
            for comment in comments:
                try:
                    comment["num_likes"] = len(get_likes_comment(comment["id"], post["id"], target_host, host))
                except:
                    pass
        
            post["comments_top3"] = comments
            post["num_likes"] = len(get_likes_post(post["id"], target_host, host))
        except:
            pass

    serializer = AuthorSerializer(currentAuthor, context={'host': host})
    currentAuthor = serializer.data
    context = {
        'host':host,
        'author_id' : currentAuthor["url"], 
        'target_author_id' : author_id,
        'target_author' : target_author,
        'target_host' : target_host,
        'is_following': is_following,
        'is_follower': is_follower,
        'can_edit': target_host == host and (request.user.is_staff or target_id == follower_id),
        'posts': posts,
        'request_next_page': next_page,
        'request_next_page_link': abs_path_no_query + "?page=" + str(next_page) + "&size=" + str(request_size),
        'request_prev_page': prev_page,
        'request_prev_page_link': abs_path_no_query + "?page=" + str(prev_page) + "&size=" + str(request_size),
        'request_size': request_size,
        'user_author': currentAuthor
    }
    return Utils.defaultRender(request,'authors/author.html',context)

def friend_requests(request: HttpRequest):
    # Drop if not logged in
    if request.user.is_anonymous:
        return Utils.defaultRender(request,'core/index.html')

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
    return Utils.defaultRender(request, 'authors/index.html', context)

def get_3latest_comments(post_id, target_host, host):
    post_id = Utils.cleanPostId(post_id, host)
    comments = None
    if target_host == host:
        comments = Comment.objects.filter(post=post_id)[:3]
        comments = CommentSerializer(comments, context={'host': host}, many=True).data
    else:
        comments = Utils.getFromUrl(post_id+"/comments")
        if (comments.__contains__("data")):
            comments = comments["data"]

    return comments

def get_likes_post(post_id, target_host, host):
    post_id = Utils.cleanPostId(post_id, host)
    likes = None
    if target_host == host:
        likes = Like.objects.filter(post=post_id)
        likes = CommentSerializer(likes, context={'host': host}, many=True).data
    else:
        likes = Utils.getFromUrl(post_id+"/likes")
        if (likes.__contains__("data")):
            likes = likes["data"]

    return likes

def get_likes_comment(comment_id, post_id, target_host, host):
    comment_id = Utils.cleanCommentId(str(comment_id), host)
    likes = None
    if target_host == host:
        likes = Like.objects.filter(comment=comment_id)
        likes = CommentSerializer(likes, context={'host': host}, many=True).data
    else:
        if (not Utils.getUrlHost(comment_id)):
            comment_id = post_id + "/comments/" + comment_id
        likes = Utils.getFromUrl(comment_id+"/likes")
        if (likes.__contains__("data")):
            likes = likes["data"]

    return likes

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