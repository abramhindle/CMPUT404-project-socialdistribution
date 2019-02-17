from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..models import Category
from ..serializers import PostSerializer


class CreatePostView(generics.GenericAPIView):
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        input_category_list = request.data.getlist("categories")

        for category in input_category_list:
            if (not Category.objects.filter(name=category).exists()):
                new_category = Category(name=category)
                new_category.save()

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user.authorprofile)
            return Response("Create Post Success", status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

