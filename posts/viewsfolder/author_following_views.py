from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework import views, status
from rest_framework.response import Response
from posts.helpers import get_follow, get_friends, get_follow_request, get_user
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from posts.models import Follow, FollowRequest, User
from posts.serializers import FollowSerializer, FollowRequestSerializer


class AuthorViewFriendRequests(TemplateView):

    @method_decorator(login_required)
    def get(self, request):
        follow_requests = FollowRequest.objects.filter(requestee=request.user)

        return render(request, template_name='author/author_follow_requests.html',
                      context={'follow_requests': follow_requests})

    @method_decorator(login_required)
    def post(self, request):
        """
        Approves a follow request from another user. Will delete the follow request and will create a follow
        going from current user -> follower
        :param request:
        :param follower:
        :return: """
        follower = get_user(request.POST.get('follow_target', ''))
        user = request.user
        follow_request = get_follow_request(user.id, follower.id)
        # Delete follow request
        if follow_request:
            follow_request.delete()

        # create a follow relation
        followSerializer = FollowSerializer(data={}, context={'followee': follower.id, 'follower': user.id})
        if followSerializer.is_valid():
            follow = followSerializer.save()
        follow_requests = FollowRequest.objects.filter(requestee=request.user)
        return HttpResponseRedirect(reverse('frontendfriendrequests'))


    @method_decorator(login_required)
    def delete(self, request, follower):
        """
        Reject the friend requests from a user.
        :param request:
        :param follower:
        :return:
        """
        follow_request = get_follow_request(request.user.id, follower)
        if follow_request:
            follow_request.delete()
        return render(request, status=status.HTTP_204_NO_CONTENT)


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
        follows = Follow.objects.filter(follower=user).values_list('followee', flat=True)
        followers = Follow.objects.filter(followee=user).values_list('follower', flat=True)
        friendIDs = follows.intersection(followers)
        listIDS = list(friendIDs)
        properOutput = [str(id) for id in listIDS]

        ## Currently not needed, but leaving in incase the mr.worldwide will require the users not just id's (which it probably will)
        # friends =[]
        # nextFriend = self.get_user(listIDS.pop())
        # while len(listIDS) > 0:
        #     friends.append(nextFriend)
        #     nextFriend = self.get_user(listIDS.pop())

        data = {
            "query": "friends",
            "authors": properOutput
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        user = self.get_user(pk)
        others = map(self.get_user, request.data['authors'])
        friends = []
        for other in others:
            if (self.are_friends(user, other)):
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
        followA = self.get_follow(author1, author2)
        followB = self.get_follow(author2, author1)
        authors = [str(authorid1), str(authorid2)]
        data = {
            "query": "friends",
            "authors": authors,
            "friends": False
        }
        if followA and followB:
            data['friends'] = True
        return Response(data=data, status=status.HTTP_200_OK)


class FollowView(views.APIView):
    def get_follow(self, follower, followee):
        try:
            return Follow.objects.get(followee=followee, follower=follower)
        except Follow.DoesNotExist:
            return None

    def get_user(self, userid):
        try:
            return User.objects.get(pk=userid)
        except User.DoesNotExist:
            return None

    @method_decorator(login_required)
    def delete(self, request, authorid):
        user = request.user
        other = self.get_user(authorid)
        if (user and other):
            follow = self.get_follow(follower=user.id, followee=other.id)
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


"""
Get the follow requests for a user.
"""


class FollowReqListView(views.APIView):
    def get_followrequests(self, user):
        try:
            reqs = FollowRequest.objects.filter(requestee=user)
            return reqs
        except FollowRequest.DoesNotExist:
            return []

    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        reqs = self.get_followrequests(user)
        listIDS = list(reqs.values_list('requester', flat=True))
        properOutput = [str(id) for id in listIDS]
        # TODO Delete follow requests if declined.
        data = {
            "query": "friendrequests",
            "author": user.id,
            "authors": properOutput
        }
        return Response(status=status.HTTP_200_OK, data=data)


class FriendRequestView(views.APIView):
    """Make a friend request to a user"""

    def try_get_follow(self, user, other):
        try:
            Follow.objects.get(followee=other, follower=user)
            return True
        except Follow.DoesNotExist:
            return False

    def post(self, request):
        user = request.data.get("author")
        other = request.data.get("friend")
        if user is None or other is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if user is not None and other is not None:
            try:
                user_obj = User.objects.get(pk=user)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            try:
                other_obj = User.objects.get(pk=other)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        followSerializer = FollowSerializer(data=request.data, context={'followee': other, 'follower': user})
        if followSerializer.is_valid():
            follow = followSerializer.save()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if (self.try_get_follow(user=other_obj, other=user_obj)):
            followRequest = Follow.objects.get(followee=user_obj.id, follower=other_obj.id)
            return Response(status=status.HTTP_201_CREATED, data={'follow': follow, 'followRequest': followRequest})
        reqSerializer = FollowRequestSerializer(data=request.data,
                                                context={'create': True, 'requestee': other, 'requester': user})
        if reqSerializer.is_valid():
            followRequest = reqSerializer.save()
            follow = FollowSerializer(follow)
            return Response(status=status.HTTP_201_CREATED,
                            data={'follow': follow.data, 'followRequest': reqSerializer.data})
        return Response(status=status.HTTP_400_BAD_REQUEST)
