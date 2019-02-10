from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..serializers import PostSerializer, UserSerializer, LoginUserSerializer
from rest_framework.views import APIView
from ..models import Post


class PostView(generics.GenericAPIView):
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        print("hii")
        posts = Post.objects.all()
        print(posts)
        aa = self.request.user.posts.all()
        print(aa)
        print("^this is aa")
        serializer = PostSerializer(posts, many=True)
        print(serializer.data)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # user = serializer.validated_data
        # return Response({
        #     "user": UserSerializer(user, context=self.get_serializer_context()).data
        # })
        print("this is post request")
        print(self.request.user)
        print(request.data)
        serializer = PostSerializer(data=request.data, context={'request': self.request})
        print("before is valid")
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("after is valid")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

