from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework import views, status
from rest_framework.response import Response
from posts.helpers import get_follow_request, get_user, get_local_user, get_ww_user, is_local_user
from posts.helpers import get_follow, get_friends, get_follow_request, get_user, parse_id_from_url
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from posts.models import Follow, FollowRequest, User, WWUser, Server
from posts.serializers import FollowSerializer, FollowRequestSerializer, UserSerializer
from urllib.parse import urlparse


class AuthorViewFriendRequests(TemplateView):

    @method_decorator(login_required)
    def get(self, request):
        ww_user = get_ww_user(request.user.id)
        follow_requests = FollowRequest.objects.filter(requestee=ww_user)

        return render(request, template_name='author/author_follow_requests.html',
                      context={"author_id": request.user.id, 'follow_requests': follow_requests})


class AuthorViewFollowing(TemplateView):

    @method_decorator(login_required)
    def get(self, request):
        following = Follow.objects.filter(follower=request.user.id)
        return render(request, template_name="author/author_following.html", context={'following': following})

class FriendListView(views.APIView):
    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    def get_follow(self, follower, followee):
        try:
            Follow.objects.get(followee=followee, follower=follower)
            return True
        except Follow.DoesNotExist:
            return False

    def are_friends(self, user, other):

        followA = self.get_follow(user, other)
        followB = self.get_follow(other, user)
        if followA and followB:
            return True
        else:
            return False

    def get(self, request, pk):
        user = self.get_user(pk)
        if user == None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        ww_user = get_ww_user(user.id)
        follows = Follow.objects.filter(follower=ww_user).values_list('followee', flat=True)
        friends = []
        for follow in follows:
            if is_local_user(follow):
                if self.get_follow(followee=ww_user, follower=follow):
                    friends.append(follow)
            else:
                friends.append(follow)
        properOutput = [str(id) for id in friends]

        data = {
            "query": "friends",
            "authors": properOutput
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        user = self.get_user(pk)
        ww_user = WWUser.objects.get(user_id=user.id)
        others = map(self.get_user, request.data['authors'])
        friends = []
        for other in others:
            ww_other = WWUser.objects.get(user_id=other.id)
            if (self.are_friends(ww_user, ww_other)):
                friends.append(other)
        data = request.data
        data['authors'] = [str(friend.id) for friend in friends]
        return Response(data=data, status=status.HTTP_200_OK)


class AreFriendsView(views.APIView):
    def get_follow(self, follower, followee):
        try:
            Follow.objects.get(followee=followee, follower=follower)
            return True
        except Follow.DoesNotExist:
            return False

    def get_user(self, userid):
        try:
            return User.objects.get(pk=userid)
        except User.DoesNotExist:
            return None

    def get(self, request, authorid1, authorid2, service2=None):
        author1, author2 = map(self.get_user, [authorid1, authorid2])
        if author1 is None or author2 is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        ww_author1, ww_author2 = map(get_ww_user, [authorid1, authorid2])
        followA = self.get_follow(ww_author1, ww_author2)
        followB = self.get_follow(ww_author2, ww_author1)
        authors = [str(authorid1), str(authorid2)]
        data = {
            "query": "friends",
            "authors": authors,
            "friends": False
        }
        if followA and followB:
            data['friends'] = True
        return Response(data=data, status=status.HTTP_200_OK)

class FollowReqListView(views.APIView):
    """
    Get the follow requests for a user.
    """

    def get_followrequests(self, user):
        try:
            reqs = FollowRequest.objects.filter(requestee=user)
            return reqs
        except FollowRequest.DoesNotExist:
            return []

    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        user_serialized = UserSerializer(instance=user)
        ww_user = get_ww_user(user.id)
        reqs = self.get_followrequests(ww_user)
        listIDS = list(reqs.values_list('requester', flat=True))
        properOutput = [str(id) for id in listIDS]
        # TODO Delete follow requests if declined.
        data = {
            "query": "friendrequests",
            "author": user_serialized.data['id'],
            "authors": properOutput
        }
        return Response(status=status.HTTP_200_OK, data=data)

    @method_decorator(login_required)
    def post(self, request, authorid):
        ww_user = get_ww_user(request.user.id)
        ww_followee = WWUser.objects.get(user_id=authorid)
        followSerializer = FollowSerializer(data=request.data,
                                            context={'followee': ww_followee, 'follower': ww_user})
        if followSerializer.is_valid():
            followSerializer.save()
        follow_req = FollowRequest.objects.get(requester=ww_followee, requestee=ww_user)
        follow_req.delete()

        return Response(status=status.HTTP_200_OK)

    @method_decorator(login_required)
    def delete(self, request, authorid):

        ww_user = get_ww_user(user_id=request.user.id)
        ww_other = get_ww_user(user_id=authorid)
        follow_request = get_follow_request(requestee=ww_user,requester=ww_other)
        if follow_request:
            follow_request.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class FollowView(views.APIView):


    @method_decorator(login_required)
    def delete(self, request, authorid):
        user = request.user
        other = get_user(authorid)
        local_other = (get_local_user(authorid) is not None)
        if (user and other):
            ww_user = get_ww_user(user_id=user.id)
            ww_other = get_ww_user(user_id=other.id)
            follow = get_follow(follower=ww_user, followee=ww_other)
            if follow is not None:
                follow.delete()
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            follow_request = get_follow_request(other.id, user.id)
            if follow_request:
                follow_request.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class FriendRequestView(views.APIView):
    """Make a friend request to a user"""

    def try_get_follow(self, user, other):
        try:
            Follow.objects.get(followee=other, follower=user)
            return True
        except Follow.DoesNotExist:
            return False

    def post(self, request):
        # Author = IS the person requesting
        # Friend = The person who is being requested
        user = request.data.get("author")
        ww_author = WWUser.objects.get_or_create(url=user.get('id'), user_id=parse_id_from_url(user.get('id')))[0]
        friend = request.data.get("friend")
        ww_friend = WWUser.objects.get_or_create(url=friend.get('id'), user_id=friend.get('id').split('/author/')[1])[0]
        # only care if follower is local
        if ww_friend.local == False and ww_author.local == True:
            # Send request
            followSerializer = FollowSerializer(data=request.data,
                                                context={'followee': ww_friend, 'follower': ww_author})
            followSerializer.is_valid()
            followSerializer.save()
            external_host = ww_friend.url.split('/author')[0]
            server = Server.objects.get(server=external_host)
            server.send_external_friendrequest(friend, user)
            # Yeet it away
            return Response(status=status.HTTP_204_NO_CONTENT)
        if ww_friend.local == False and ww_author.local == False:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if ww_friend.local and not ww_author.local:
            if self.try_get_follow(user=ww_friend, other=ww_author):
                return Response(status=status.HTTP_204_NO_CONTENT)
            if FollowRequest.objects.filter(requester=ww_author.url, requestee=ww_friend.url).exists():
                return Response(status=status.HTTP_204_NO_CONTENT)
            reqSerializer = FollowRequestSerializer(data=request.data,
                                                    context={'create': True, 'requestee': ww_friend,
                                                             'requester': ww_author})
            if reqSerializer.is_valid():
                reqSerializer.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
        if ww_friend.local and ww_author.local:
            followSerializer = FollowSerializer(data=request.data,
                                                context={'followee': ww_friend, 'follower': ww_author})
            followSerializer.is_valid()
            followSerializer.save()
            if self.try_get_follow(user=ww_friend, other=ww_author):
                return Response(status=status.HTTP_204_NO_CONTENT)
            if FollowRequest.objects.filter(requestee=ww_author.url, requester=ww_friend.url).exists():
                return Response(status=status.HTTP_204_NO_CONTENT)
            reqSerializer = FollowRequestSerializer(data=request.data,
                                                    context={'create': True, 'requestee': ww_friend,
                                                             'requester': ww_author})
            if reqSerializer.is_valid():
                reqSerializer.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

