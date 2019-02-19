from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..models import Category
from ..serializers import PostSerializer
from django.http import QueryDict


class CreatePostView(generics.GenericAPIView):
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def insert_post(self, request):
        print("inside the postit boi")
        # input_category_list = request.data.getlist("categories")
        # print(request.data, "save me")
        for category in input_category_list:
            if (not Category.objects.filter(name=category).exists()):
                Category.objects.create(name=category)

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user.authorprofile)
            return Response("Create Post Success", status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        print("post")
        print(request.data)
        return self.insert_post(request)

    def put(self, request, postid):
        # print(request, "put boi")
        # print(request.body)
        # print(QueryDict(request.body))
        # print(request.user, "save me fam")
        # print("nani")
        if 
        return self.insert_post(QueryDict(request.body))
