from rest_framework import generics, permissions, status
from django.db import transaction
from rest_framework.response import Response
from ..models import Category
from ..serializers import PostSerializer
import json

class CreatePostView(generics.GenericAPIView):
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)
    test_list = []

    def insert_post(self, request, user):
        # print(request, "save me")
        input_category_list = request.getlist("categories")
        self.test_list.append(request)
  
        # print(request.data, "save me")
        for category in input_category_list:
            if (not Category.objects.filter(name=category).exists()):
                Category.objects.create(name=category)

        serializer = PostSerializer(data=request)
        # print(serializer)
        if serializer.is_valid():
            # print("am i valid")
            serializer.save(author=user.authorprofile)
            return Response("Create Post Success", status.HTTP_200_OK)
        else:
            # print("or am i not valid")
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        # print(request.user, "post user")
        print("\n",request.data, "dreaming")
        return self.insert_post(request.data, request.user)

    def put(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                if ("categories" in request.data.keys() and len(request.data["categories"]) > 0):
                    input_category_list = request.data["categories"]
                    for category in input_category_list:
                        if (not Category.objects.filter(name=category).exists()):
                            Category.objects.create(name=category)
                else:
                    raise ValueError("Categories must be provided")

                if ("visibleTo" in request.data.keys()):
                    visible_to_list = request.data["visibleTo"]
                    if (len(visible_to_list) > 0 and request.data.get("visibility") != "PRIVATE"):
                        raise ValueError("Error: Post must be private if visibleTo is provided")

                    for author in visible_to_list:
                        author_profile_id = author.split("/")[-1]
                        # todo: check if user belongs to other server
                        if (not AuthorProfile.objects.filter(id=author_profile_id).exists()):
                            raise ValueError("Error: User in visibleTo does not exist")
                        if (not AllowToView.objects.filter(user_id=author).exists()):
                            AllowToView.objects.create(user_id=author)
        except ValueError as error:
            return Response(str(error), status.HTTP_400_BAD_REQUEST)

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user.authorprofile)
            return Response("Create Post Success", status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
