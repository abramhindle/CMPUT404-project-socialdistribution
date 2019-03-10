from django.db import transaction
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..models import Category, Post, AuthorProfile, AllowToView
from ..serializers import PostSerializer


class CreatePostView(generics.GenericAPIView):
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        query_set = Post.objects.filter(visibility="PUBLIC")
        posts = PostSerializer(query_set, many=True).data
        response_data = {
            "query": "posts",
            "count": len(posts),
            "posts": posts
        }
        return Response(response_data, status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
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

    def delete(self, request, postid=""):
        if (postid == ""):
            return Response("Error: Post ID is Missing", status.HTTP_400_BAD_REQUEST)
        post_id = self.kwargs["postid"]
        try:
            post = Post.objects.get(id=post_id)
            if (request.user.authorprofile.id != post.author.id):
                return Response("Error: Invalid Author", status.HTTP_400_BAD_REQUEST)

            Post.objects.filter(id=post_id).delete()
            return Response("Delete Post Success", status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response("Error: Post Does Not Exist", status.HTTP_400_BAD_REQUEST)
