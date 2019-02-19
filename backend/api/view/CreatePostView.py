from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..models import Category, Post
from ..serializers import PostSerializer


class CreatePostView(generics.GenericAPIView):
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        query_set = Post.objects.filter(visibility="PUBLIC")
        print(query_set)
        response_data = PostSerializer(query_set, many=True).data
        print("response data")
        print(response_data)
        print("index 0")
        print(response_data[0])
        print(len(response_data))
        return Response(response_data, status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        input_category_list = request.data.getlist("categories")

        for category in input_category_list:
            if (not Category.objects.filter(name=category).exists()):
                Category.objects.create(name=category)

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user.authorprofile)
            return Response("Create Post Success", status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
