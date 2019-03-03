from rest_framework import views, status
from rest_framework.response import Response
from django.http import Http404
from .models import User, Follow
from .serializers import UserSerializer,FollowSerializer
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
    
    def post(self, request):
        serializer = FollowSerializer(data=request.data,content={'create': False})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
