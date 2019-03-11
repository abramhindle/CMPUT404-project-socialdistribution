from rest_framework import views, status
from rest_framework.response import Response
from django.http import Http404
from .models import User, Follow, Post, Comment, Category, FollowRequest
from .serializers import UserSerializer, UserSerializer, PostSerializer, CommentSerializer,FollowSerializer, FollowRequestSerializer
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
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
                return Response(status=status.HTTP_404_NOT_FOUND)
            try:
                other_obj = User.objects.get(id=other['id'])
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        followSerializer = FollowSerializer(data=request.data, context={'create':True,'followee':other,'follower':user})
        if followSerializer.is_valid():
            follow = followSerializer.save()
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if(self.try_get_follow(user=other_obj,other=user_obj)):
            followRequest = Follow.objects.get(followee=user_obj,follower=other_obj)
            return Response(status=status.HTTP_201_CREATED, data={'follow':follow, 'followRequest':followRequest})
        reqSerializer = FollowRequestSerializer(data=request.data, context={'create':True,'requestee':other,'requester':user})
        if reqSerializer.is_valid():
            followRequest= reqSerializer.save()
            return Response(status=status.HTTP_201_CREATED, data={'follow':follow, 'followRequest':followRequest})
        return Response(status=status.HTTP_404_NOT_FOUND)

class FriendListView(views.APIView):
    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

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

# class AreFriendsView(views.APIView):
#     def get_follow(self, follower, followee):
#         try:
#             return Follow.objects.get(followee=followee,follower=follower)
#         except Follow.DoesNotExist:
#             return False

#     def get_user(self,userid):
#         try:
#             return User.objects.get(pk=userid)
#         except User.DoesNotExist:
#             return None

#     def get(self, request, authorid1, authorid2, service2=None):
#         if(service2==None):
#             onetoTwo = self.get_follow(followee=self.get_user(authorid1),follower=self.get_user(authorid2))
#             twotoOne  = self.get_follow(followee=self.get_user(authorid2),follower=self.get_user(authorid1))
#             #TODO: return authorid's and boolean saying TRUE
#             friends = onetoTwo and twotoOne
#             return Response({"friends:%s"%friends})
#         else:
#             #TODO:
#             # get_follow for our local user follow
#             onetoTwo = self.get_follow(followee=self.get_user(authorid1),follower=self.get_user(authorid2))
#             # Make request to service 2
            
#             # getFriendList for the external user
#             # compare if both following
#             data = {}
#             data["authors"]=[author1,author2]
#             data["friends"]=False 
#             return Response(data)

# TODO: (<AUTHENTICATION>) Make sure author is approved

class PostView(views.APIView):
    @method_decorator(login_required)
    def post(self, request):
        """
        Create new categories
        """
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

        serializer = PostSerializer(data=request.data, context={'user':request.user})
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

    @method_decorator(login_required)
    def delete(self, request, pk):

        # request.user
        post_obj = Post.objects.get(pk=pk)
        if post_obj.author == request.user:
            post = self.get_post(pk)
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class CommentViewList(views.APIView):

    # TODO: (<AUTHENTICATION>, <VISIBILITY>) check VISIBILITY before posting
    #@method_decorator(login_required)
    def post(self, request, post_id):
        serializer = CommentSerializer(data=request.data, context={'post_id':post_id, 'user':request.user})
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

