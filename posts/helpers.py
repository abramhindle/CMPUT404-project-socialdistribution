from .models import *
from django.http import Http404
from urllib.parse import urlparse
from .serializers import UserSerializer
from django.contrib.sites.models import Site

def get_user( pk):
        try:
            return User.objects.get(pk=pk)
        except:
            raise Http404

"""
Parses a user id from user urls in the form:
https://example.com/author/f3be7f78-d878-46c5-8513-e9ef346a759d/
"""
def parse_id_from_url(url):
    parsed = urlparse(url)
    path = parsed.path.strip('/')
    path = path.split('/')
    return path[-1]

def get_url(user):
    # TODO: When the serializer is unfucked regarding domain this should use the serializer to spit out the url :)
    # YES this shouldn't be localhost but let's talk when the urls for authors stop being strange 
    userSerializer = UserSerializer()
    return  userSerializer.get_absolute_url(user)

def get_follow( follower, followee):
    try:
        return Follow.objects.get(followee=followee, follower=follower)
    except Follow.DoesNotExist:
        return False

def are_friends(user,other):
    followA = get_follow(user,other)
    followB = get_follow(other,user)
    if followA and followB:
        return True
    else:
        return False

def get_friends(user):
    follows = Follow.objects.filter(follower=user).values_list('followee', flat=True)
    followers = Follow.objects.filter(followee=user).values_list('follower', flat=True)
    friendIDs = follows.intersection(followers)
    return friendIDs

def are_FOAF(user, other):

    userfriends = get_friends(user)
    otherfriends = get_friends(other)
    bridges = userfriends.intersection(otherfriends)
    return bridges.exists()

def get_friendship_level(user,other):

    if(are_friends(user,other)):
        return ['FRIENDS', 'FOAF']
    if(are_FOAF(user,other)):
        return ['FOAF']
    return []

def get_follow_request(followee, follower):
    try:
        return FollowRequest.objects.get(requestee=followee, requester=follower)
    except FollowRequest.DoesNotExist:
        return False

def get_follow_request_id(id):
    try:
        return FollowRequest.objects.get(id)
    except FollowRequest.DoesNotExist:
        return False

def has_private_access(user,post):
    try:
        url = get_url(user)
        val =  Viewer.objects.get(post=post,url=get_url(user))
        return True
    except Viewer.DoesNotExist:
        return False

def is_local_user(url):
    userHost = urlparse(url).hostname
    return (userHost == Site.objects.get_current().domain)

def visible_to(post,user, direct=False, local=True):
    author = get_user(post.author.id)
    if (user == author):
        return True
    if ((not direct) and post.unlisted):
        return False
    if(post.visibility=="PUBLIC" or post.visibility=="SERVERONLY"):
        return True
    f_level = get_friendship_level(user,author)
    if(post.visibility== "FRIENDS" and not("FRIENDS" in f_level)):
        return False
    if(post.visibility== "FOAF" and not("FOAF" in f_level)):
        return False
    if(post.visibility=="PRIVATE" and not has_private_access(user,post)):
        return False
    return True
    
