from rest_framework import views, status
from rest_framework.response import Response
#import requests
from django.http import Http404
from .models import User, Follow, Post, Comment, Category, FollowRequest
from .serializers import UserSerializer, UserSerializer, PostSerializer, CommentSerializer,FollowSerializer, FollowRequestSerializer
from django.views.generic import TemplateView
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template import loader
from django.shortcuts import render
import commonmark
# Create your views here.

class UserView(views.APIView):

    def get_user(self, user):
        try:
            return User.objects.get(pk=user.pk)
        except User.DoesNotExist:
            raise Http404

    def post(self, request):
        serializer = UserSerializer(data=request.data, context={'create': True})
        if serializer.is_valid() and request.user.is_anonymous:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(login_required)
    def get(self, request):
        user = self.get_user(request.user)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @method_decorator(login_required)
    def put(self, request):
        user = self.get_user(request.user)
        serializer = UserSerializer(user, data=request.data, partial=True, context={'create':False})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FriendRequestView(views.APIView):
    def try_get_follow(self, user, other):
        try:
            Follow.objects.get(followee=other,follower=user)
            return True
        except Follow.DoesNotExist:
            return False

    def post(self, request):
        user = request.data.get("author")
        other = request.data.get("friend")
        if user is not None and other is not None:
            try:
                user_obj = User.objects.get(id=user['id'])
            except User.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            try:
                other_obj = User.objects.get(id=other['id'])
            except User.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        followSerializer = FollowSerializer(data=request.data, context={'followee':other,'follower':user})
        if followSerializer.is_valid():
            follow = followSerializer.save()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if(self.try_get_follow(user=other_obj,other=user_obj)):
            followRequest = Follow.objects.get(followee=user_obj,follower=other_obj)
            return Response(status=status.HTTP_201_CREATED, data={'follow':follow, 'followRequest':followRequest})
        reqSerializer = FollowRequestSerializer(data=request.data, context={'create':True,'requestee':other,'requester':user})
        if reqSerializer.is_valid():
            followRequest= reqSerializer.save()
            return Response(status=status.HTTP_201_CREATED, data={'follow':follow, 'followRequest':followRequest})
        return Response(status=status.HTTP_400_BAD_REQUEST)

class FriendListView(views.APIView):
    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    def get_follow(self, follower, followee):
        try:
            Follow.objects.get(followee=followee,follower=follower)
            return True
        except Follow.DoesNotExist:
            return False

    def are_friends(self, user,other):

        followA = self.get_follow(user,other)
        followB = self.get_follow(other,user)
        if followA and followB:
            return True
        else:
            return False

    def get(self, request,pk):
        user = self.get_user(pk)
        if user == None:
            return  Response( status=status.HTTP_400_BAD_REQUEST)
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
            "query":"friends",
            "authors": properOutput
        }
        return Response(data=data,status=status.HTTP_200_OK )

    def post(self, request, pk):
        user = self.get_user(pk)
        others = map(self.get_user,request.data['authors'])
        friends = []
        for other in others:
            if(self.are_friends(user,other)):
                friends.append(other)
        data = request.data
        data['authors']= [str(friend.id) for friend in friends]
        return Response(data=data, status=status.HTTP_200_OK )

class AreFriendsView(views.APIView):
    def get_follow(self, follower, followee):
        try:
            Follow.objects.get(followee=followee,follower=follower)
            return True
        except Follow.DoesNotExist:
            return False

    def get_user(self,userid):
        try:
            return User.objects.get(pk=userid)
        except User.DoesNotExist:
            return None

    def get(self, request, authorid1, authorid2, service2=None):
        author1, author2 = map(self.get_user,[authorid1,authorid2])
        if author1 is None or author2 is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        followA = self.get_follow(author1,author2)
        followB = self.get_follow(author2,author1)
        authors = [str(authorid1),str(authorid2)]
        data = {
                "query":"friends",
                "authors": authors,
                "friends": False
        }
        if followA and followB:
            data['friends']=True
        return Response(data=data,status=status.HTTP_200_OK)


class FollowView(views.APIView):
    def get_follow(self, follower, followee):
        try:
            return Follow.objects.get(followee=followee,follower=follower)
        except Follow.DoesNotExist:
            return None

    def get_user(self,userid):
        try:
            return User.objects.get(pk=userid)
        except User.DoesNotExist:
            return None

    @method_decorator(login_required)
    def delete(self,request,authorid):
        user = request.user
        other = self.get_user(authorid)
        if(user and other):
            follow = self.get_follow(follower=user.id,followee=other.id)
            if(follow is not None):
                follow.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class AdminUserView(TemplateView):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        unapproved = User.objects.filter(approved=False)

        return render(request, 'users/approve_user.html', context={'unapproved': unapproved})

    @method_decorator(login_required)
    def post(self, request):
        if not request.user.is_staff:
            raise PermissionDenied
        user_to_approve = request.POST['user']
        user = User.objects.get(id=user_to_approve)
        user.approved = True
        user.save()
        unapproved = User.objects.filter(approved=False)

        return render(request, 'users/approve_user.html', context={'unapproved': unapproved})


# TODO: (<AUTHENTICATION>) Make sure author is approved

class PostView(views.APIView):
    @method_decorator(login_required)
    def post(self, request):
        """
        Create new categories
        """
        if not request.user.approved:
            raise PermissionDenied
        categories = request.data.get("categories")
        if categories is not None:
            # author has defined categories
            for cat in categories:
                # check if category exists
                try:
                    cat_obj = Category.objects.get(category=cat)
                except Category.DoesNotExist:
                    cat_obj = None

                if cat_obj is None:
                    Category.objects.create(category=cat)

        serializer = PostSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO: (<AUTHENTICATION>, <VISIBILITY>) check VISIBILITY before getting
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class FollowReqListView(views.APIView):
    def get_followrequests(self,user):
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
        data = {
            "query":"friendrequests",
            "author":user.id,
            "authors":properOutput
        }
        return Response(status=status.HTTP_200_OK,data=data)


class PostViewID(views.APIView):

    def get_post(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    # TODO: (<AUTHENTICATION>, <VISIBILITY>) check VISIBILITY before getting
    def get(self, request, pk):
        post = self.get_post(pk)

        serializer = PostSerializer(post)
        return Response(serializer.data)

    def post(self,request,pk):
        post = self.get_post(pk)
        if (post.visibility in ("FOAF", "Friend of a Friend")):
            authorid = post.author.id
            requester = pk
            #foaf = checkFOAF(request,requester,authorid)
            foaf = True
            if(foaf):
                serializer = PostSerializer(post)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_403_FORBIDDEN)

    @method_decorator(login_required)
    def delete(self, request, pk):

        # request.user
        post_obj = self.get_post(pk)
        if post_obj.author == request.user:
            post = self.get_post(pk)
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class FrontEndPostViewID(TemplateView):
    def get_post(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        post = self.get_post(pk)
        serializer = PostSerializer(post)
        if post.contentType == "text/markdown":
            post_content = commonmark.commonmark(post.content)
        else:
            post_content = "<p>" + post.content + "</p>"

        return render(request, 'post/post.html', context={'post': serializer.data, 'post_content': post_content})


class CommentViewList(views.APIView):

    # TODO: (<AUTHENTICATION>, <VISIBILITY>) check VISIBILITY before posting
    @method_decorator(login_required)
    def post(self, request, post_id):
        if not request.user.approved:
            raise PermissionDenied
        serializer = CommentSerializer(data=request.data, context={'post_id': post_id, 'user': request.user})
        # print(serializer.initial_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO: (<AUTHENTICATION>, <VISIBILITY>) check VISIBILITY before getting
    def get(self, request, post_id):
        comments = Comment.objects.filter(parent_post_id=post_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

# def checkFOAF(request, userid,authorid):

#     claimedFriends = request.data['friends']
#     userData = {
# 	    "query":"friends",
# 	    "author":userid,
# 	    "authors": claimedFriends
#     }
#     url = str(userid)+"/friends/"
#     # Make POST request to url, with userData above, 

#     bridges= response.data['authors']

#     authorData = {
# 	    "query":"friends",
# 	    "author":userid,
#         "authors": bridges
#     }
#     url = str(authorid)+"/friends/"
    
#     # Make POST request to url, with authorData above

#     bridges= response.data['authors']
#     if bridges ==[]:
#         return False
#     # If bridges is [] at this point, they can't access it
#     for bridge in bridges:
#         bridgeData = {
#             "query":"friends",
# 	        "author":bridge,
#             "authors": [userid,authorid]
#         }
#         url = str(bridge)+"/friends/"
#         if(set(response.data['authors'])==set([userid,authorid])):
#             return True

#     return False

