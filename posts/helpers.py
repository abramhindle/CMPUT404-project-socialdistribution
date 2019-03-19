from .models import *
from django.http import Http404

def get_user( pk):
        try:
            return User.objects.get(pk=pk)
        except:
            raise Http404

def get_follow( follower, followee):
    if not (follower.is_authenticated() and followee.is_authenticated()):
        return False
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
