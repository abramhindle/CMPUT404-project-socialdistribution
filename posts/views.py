from rest_framework import views, status
from rest_framework.response import Response
from django.http import Http404
from .models import User, Follow, Post, Comment, Category
from .serializers import UserSerializer,FollowSerializer, FollowRequestSerializer, UserSerializer, PostSerializer, CommentSerializer
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

class FollowView(views.APIView):
    def get_follow(self, request):
        try:
            return Follow.objects.get(follower=request.follower, followee=request.followee)
        except Follow.DoesNotExist:
            return Http404
    
    def get(self, request):
        follow = self.get_follow(request.follow)
        serializer = FollowSerializer(follow)
        return Response(serializer.data)
    
class FriendListView(views.APIView):
    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_user(pk)
        follows = Follow.objects.get(followee=user.id)
        if follows.exists():
            followedBy  = follows.get(follower=user.id)
            if followedBy.exists():
                serializer = FollowSerializer(followedBy, many=True)
                return Response(serializer.data)
            else:
                serializer = FollowSerializer({}, many=True)
                return Response(serializer.data)
        else:
            serializer = FollowSerializer({}, many=True)
            return Response(serializer.data)


class AreFriendsView(views.APIView):
    def get_follow(self, follower, followee):
        try:
            return Follow.objects.get(followee=followee,follower=follower)
        except Follow.DoesNotExist:
            return False
    
    def get(self, request, authorid1, service2, authorid2 ):
        onetoTwo = self.get_follow(followee=authorid1,follower=authorid2)
        twotoOne  = self.get_follow(followee=authorid2,follower=authorid1)
        #TODO: return authorid's and boolean saying TRUE
        friends = onetoTwo and twotoOne
        return Response({"friends:%s"%friends})
class FriendRequestView(views.APIView):

    def post(self, request):
        # This creates author follows disired friend, and sends a friend req to the followee
        serializer = FollowSerializer(request.data)
        serializerReq = FollowRequestSerializer(request.data)
        if serializer.is_valid() and serializerReq.is_valid():
            serializer.save()
            serializerReq.save()                
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
