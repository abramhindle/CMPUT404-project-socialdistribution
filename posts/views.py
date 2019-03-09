from rest_framework import views, status
from rest_framework.response import Response
from django.http import Http404
from .models import User, Follow
from .serializers import UserSerializer,FollowSerializer, FollowRequestSerializer
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
        followedBy  = follows.get(follower=user.id)
        serializer = FollowSerializer(followedBy, many=True)
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
        return Response()

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